from typing import Type, List
import click
from pulumi import automation as auto
from app_util.builder import AppBuilder, Builds
from app_util.deployer import AppDeployer
from test_runner import TestRunner
import os
from util.result import AppResult, Result, sanitize_result_key
from util.logging import PulumiLogging, configureLoggers
import subprocess
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
    configureLoggers(run_id)
    result_code = 0

    log.info(f'Starting run with id: {run_id}')
    # pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    appResults = {str: AppResult}
    for directory in directories.split(","):
        run_single(directory, region, disable_tests, provider, appResults, run_id)
    #     pool.submit(run_single(directory, region, disable_tests, provider, appResults))
    # pool.shutdown(wait=True)

    for key in appResults:
        result: AppResult = appResults[key]
        if result.result != Result.SUCCESS:
            result_code = 1
        log.info(result.to_string())

    exit(result_code)


def run_single(directory: str, region: str, disable_tests: List[str], provider: str, appResults: dict[Type[str], Type[AppResult]], run_id: str):
    try:
        os.environ['PULUMI_CONFIG_PASSPHRASE'] = ""
        builder = AppBuilder(directory, provider)

        config_base_path = os.path.join("apps", directory, "config", provider)
        files: list[str] = os.listdir(config_base_path)
        upgrade = False
        stack: auto.Stack = None
        pulumi_logger = PulumiLogging(run_id, directory)

        for file in files:
            path = os.path.join(config_base_path, file)
            if not os.path.isfile(path):
                log.debug(f'{path} is not a file. Skipping run.')
                continue

            pulumi_logger.set_file_name(f'{file}.txt')
            log.info(f'Running on path {path}')
            if not upgrade:
                result_key = sanitize_result_key(f'{path}-{Builds.RELEASE}')
                appResults[result_key] = AppResult(path, Builds.RELEASE, Result.STARTED)
                log.info(f'Building release application for path {path}')
                # Build the app with klotho's released version and configure the pulumi config
                stack = build_app(builder, path, appResults, upgrade, stack)
                if stack is None:
                    continue

                deployer = AppDeployer(stack, region, pulumi_logger)
                log.info(f'Configuring and deploying app {builder.cfg.app_name}')
                api_url: str = deployer.configiure_and_deploy(builder.cfg)
                if api_url == "":
                    appResults[result_key].set_result(Result.DEPLOYMENT_FAILED)
                else:
                    test_runner = TestRunner(builder.app_name, api_url, upgrade, disable_tests)
                    test_results = test_runner.run()
                    for test_result in test_results:
                        log.info(test_result.to_string())
                    appResults[result_key].add_test_results(test_results)
                upgrade = True
                raise("well exit here")
                
            # Build the app with klotho's mainline version and configure the pulumi config
            stack = build_app(builder, path, appResults, upgrade, stack)
            result_key = sanitize_result_key(f'{path}-{Builds.MAINLINE}')
            appResults[result_key] = AppResult(path, Builds.MAINLINE, Result.STARTED)
            if stack is None:
                continue

            deployer = AppDeployer(stack, region, pulumi_logger)
            api_url: str = deployer.configiure_and_deploy(builder.cfg)
            if api_url == "":
                appResults[result_key].set_result(Result.DEPLOYMENT_FAILED)
                continue

            test_runner = TestRunner(builder.app_name, api_url, upgrade, disable_tests)
            test_results = test_runner.run()
            for test_result in test_results:
                log.info(test_result.to_string())
            appResults[result_key].add_test_results(test_results)
    except Exception as e:
        log.error(e)
        for i in range(0,5):
            try:
                log.info(f'Destroying stack {stack.name}')
                pulumi_logger.set_file_name(f'destroy.txt')
                stack.destroy(on_output=pulumi_logger.log)
                log.info(f'Removing stack {stack.name}')
                result: subprocess.CompletedProcess[bytes] = subprocess.run(["pulumi", "stack", "rm", "-s", stack.name, "-y"])
                result.check_returncode()
            except:
                log.info(f'Refreshing stack {stack.name}')
                stack.refresh()



def build_app(builder: AppBuilder, path: str, appResults: dict[Type[str], Type[AppResult]], upgrade: bool, stack: auto.Stack) -> auto.Stack:
    build = Builds.RELEASE if not upgrade else Builds.MAINLINE
    app_built = builder.build_app(path, build)
    if not app_built:
        log.info(f'{path} {build} failed to build')
        result_key = sanitize_result_key(f'{path}-{build}')
        appResults[result_key].set_result(Result.COMPILATION_FAILED)
        return stack
    if stack is None:
        stack = builder.create_pulumi_stack()
    try:
        builder.install_npm_deps()
    except:
        return stack
    return stack


if __name__ == '__main__':
    run()
