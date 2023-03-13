import traceback
from typing import Type, List
import click
from pulumi import automation as auto
from app_util.builder import AppBuilder, Builds
from app_util.deployer import AppDeployer
from app_util.runner import AppRunner
from app_util.config import TestConfig
import os
from util.result import AppResult, Result, sanitize_result_key
from util.logging import PulumiLogging, configure_deployment_logger, configure_test_logger
import shortuuid
import logging


log = logging.getLogger("DeploymentRunner")

@click.command()
@click.option('--directories', type=str, required=True, help='The directories to be compiled')
@click.option('--region', type=str, required=True, help='The region to deploy to')
@click.option('--provider', type=str, required=True, help='The provider to test')
@click.option('--config-filenames', type=str, required=False, help='A comma separated list of names of specific config files to test')
@click.option('--no-destroy', is_flag=True, help='Set if you want to leave the stack of the tests up')
def run(directories, region, provider, config_filenames: str, no_destroy):
    run_id = shortuuid.ShortUUID().random(length=6).lower()
    configure_deployment_logger(run_id)
    result_code = 0

    config_files = config_filenames.split(",") if config_filenames is not None else []

    log.info(f'Starting run with id: {run_id}')
    # pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    appResults = {}
    for directory in directories.split(","):
        run_single(directory, region, provider, appResults, run_id, config_files, no_destroy)
    #     pool.submit(run_single(directory, region, disable_tests, provider, appResults))
    # pool.shutdown(wait=True)

    for key in appResults.keys():
        result: AppResult = appResults[key]
        if result.result != Result.SUCCESS:
            result_code = 1
        log.info(f'Result for key, {key}: {result.to_string()}')

    exit(result_code)


def run_single(directory: str, region: str, provider: str, appResults: dict[Type[str], Type[AppResult]], run_id: str, config_filenames: List[str], no_destroy: bool):
    try:
        os.environ['PULUMI_CONFIG_PASSPHRASE'] = ""
        builder = AppBuilder(directory, provider, run_id)
        pulumi_logger = PulumiLogging(run_id, builder.app_name)
        deployer = AppDeployer(region, pulumi_logger)
        app_runner = AppRunner(builder, deployer)

        config_base_path = os.path.join("apps", directory, "config", provider)
        files: list[str] = os.listdir(config_base_path)

        upgrade_path = False
        stack: auto.Stack = None
        step = 1
    
        ordered_files = determine_config_order(builder.cfg, files)
        try:
            for file in ordered_files:
                path = os.path.join(config_base_path, file)
                if not os.path.isfile(path):
                    log.debug(f'{path} is not a file. Skipping run.')
                    continue

                if file not in config_filenames and len(config_filenames) > 0:
                    continue

                upgrade_tests = False

                file_name = f'{os.path.splitext(file)[0]}.txt'
                configure_test_logger(run_id, builder.app_name, file_name)
                pulumi_logger.set_file_name(file_name)
                log.info(f'Running on path {path}')
                if not upgrade_path:
                    result_key = sanitize_result_key(f'{path}-{Builds.RELEASE}')
                    stack, result, test_results = app_runner.deploy_and_test(run_id, path, upgrade_tests, stack)
                    appResults.update({result_key: AppResult(path, Builds.RELEASE, result, test_results, step)})
                    step += 1
                    upgrade_tests = True
                    upgrade_path = True
                    
                # Build the app with klotho's mainline version and configure the pulumi config
                result_key = sanitize_result_key(f'{path}-{Builds.MAINLINE}')
                stack, result, test_results = app_runner.deploy_and_test(run_id, path, upgrade_tests, stack)
                appResults.update({result_key: AppResult(path, Builds.MAINLINE, result, test_results, step)})
                step += 1

        except Exception as e:
            log.error(e)
            log.error(traceback.print_exc())
        finally:
            if stack is not None and not no_destroy:
                deploy_succeeded = deployer.destroy_and_remove_stack(builder.output_dir)
                result = Result.SUCCESS if deploy_succeeded else Result.DESTROY_FAILED
                result_key = sanitize_result_key(f'{stack.name}-destroy')
                appResults.update({result_key: AppResult(path, None, result, test_results, step)})
    except Exception as e:
        log.error(f'Failed to configure app  run {e}')
        log.error(traceback.print_exc())

            
def determine_config_order(test_config: TestConfig, files: List[str]) -> List[str]:
    if len(test_config.order) == 0:
        return files
    order = []
    for cfg in test_config.order:
        if cfg not in files:
            log.fatal(f'{cfg} is in test_config but does not exist in files.')
            exit(1)
        else:
            order.append(cfg)
    for cfg in files:
        if cfg not in test_config.order:
            log.warn(f'{cfg} does not exist in test config, but exists in files. Adding to the end of the test run order.')
            order.append(cfg)
    return order

if __name__ == '__main__':
    run()
