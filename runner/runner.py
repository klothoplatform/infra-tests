import traceback
from typing import Type, List
import click
from pulumi import automation as auto
from app_util.builder import AppBuilder, Builds
from app_util.deployer import AppDeployer
from app_util.runner import AppRunner
import os
from util.result import AppResult, Result, sanitize_result_key
from util.logging import PulumiLogging, configure_deployment_logger, configure_test_logger
import shortuuid
import logging


log = logging.getLogger("DeploymentRunner")

@click.command()
@click.option('--directories', type=str, required=True, help='The directories to be compiled')
@click.option('--region', type=str, required=True, help='The region to deploy to')
@click.option('--disable-tests', multiple=True, help='The tests to be disabled')
@click.option('--provider', type=str, required=True, help='The provider to test')
def run(directories, region, disable_tests, provider):
    run_id = shortuuid.ShortUUID().random(length=8)
    configure_deployment_logger(run_id)
    result_code = 0

    log.info(f'Starting run with id: {run_id}')
    # pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    appResults = {}
    for directory in directories.split(","):
        run_single(directory, region, disable_tests, provider, appResults, run_id)
    #     pool.submit(run_single(directory, region, disable_tests, provider, appResults))
    # pool.shutdown(wait=True)

    for key in appResults.keys():
        result: AppResult = appResults[key]
        if result.result != Result.SUCCESS:
            result_code = 1
        log.info(result.to_string())

    exit(result_code)


def run_single(directory: str, region: str, disable_tests: List[str], provider: str, appResults: dict[Type[str], Type[AppResult]], run_id: str):
    try:
        os.environ['PULUMI_CONFIG_PASSPHRASE'] = ""
        builder = AppBuilder(directory, provider)
        pulumi_logger = PulumiLogging(run_id, builder.app_name)
        deployer = AppDeployer(region, pulumi_logger)
        app_runner = AppRunner(builder, deployer)

        config_base_path = os.path.join("apps", directory, "config", provider)
        files: list[str] = os.listdir(config_base_path)

        upgrade = False
        stack: auto.Stack = None
        step = 1


        for file in files:
            path = os.path.join(config_base_path, file)
            if not os.path.isfile(path):
                log.debug(f'{path} is not a file. Skipping run.')
                continue

            file_name = f'{os.path.splitext(file)[0]}.txt'
            configure_test_logger(run_id, builder.app_name, file_name)
            pulumi_logger.set_file_name(file_name)
            log.info(f'Running on path {path}')
            if not upgrade:
                result_key = sanitize_result_key(f'{path}-{Builds.RELEASE}')
                stack, result, test_results = app_runner.deploy_and_test(path, upgrade, stack)
                appResults[result_key] = AppResult(path, Builds.RELEASE, result, test_results, step)
                step += 1
                upgrade = True
                
            # Build the app with klotho's mainline version and configure the pulumi config
            result_key = sanitize_result_key(f'{path}-{Builds.MAINLINE}')
            stack, result, test_results = app_runner.deploy_and_test(path, upgrade, stack)
            appResults[result_key] = AppResult(path, Builds.MAINLINE, result, test_results, step)
            step += 1

    except Exception as e:
        log.error(e)
        log.error(traceback.print_exc())
    finally:
        deploy_succeeded = deployer.destroy_and_remove_stack(builder.output_dir)
        result = Result.SUCCESS if deploy_succeeded else Result.DESTROY_FAILED
        result_key = sanitize_result_key(f'{stack.name}-destroy')
        appResults[result_key] = AppResult(path, None, result, test_results, step)

            


if __name__ == '__main__':
    run()
