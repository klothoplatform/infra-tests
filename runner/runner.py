import click
import pulumi
from pulumi import automation as auto
from app_util.builder import AppBuilder, Builds
from app_util.deployer import AppDeployer
from test_runner import TestRunner
import concurrent.futures
import os
from util.result import AppResult, Result
from util.logging import log
import subprocess

@click.command()
@click.option('--directories', type=str, required=True, help='The directories to be compiled')
@click.option('--region', type=str, required=True, help='The region to deploy to')
@click.option('--disable-tests', multiple=True, help='The tests to be disabled')
@click.option('--provider', type=str, required=True, help='The provider to test')
def run(directories, region, disable_tests, provider):
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    appResults = {}
    for directory in directories.split(","):
        pool.submit(run_single(directory, region, disable_tests, provider, appResults))
    pool.shutdown(wait=True)


def run_single(directory, region, disable_tests, provider, appResults):
    os.environ['PULUMI_CONFIG_PASSPHRASE'] = ""
    builder = AppBuilder(directory, provider)

    config_base_path = os.path.join("apps", directory, "config", provider)
    files: list[str] = os.listdir(config_base_path)
    upgrade = False
    stack: auto.Stack = None

    for file in files:
        path = os.path.join(config_base_path, file)
        if not os.path.isfile(path):
            log.info(f'{path} is not a file')
            continue
        log.info(f'release is built')

        if not upgrade:
            # Build the app with klotho's released version and configure the pulumi config
            app_built = builder.build_app(path, Builds.RELEASE)
            log.info(f'{app_built} release is built')
            if not app_built:
                appResults[path] = AppResult(path, Result.COMPILATION_FAILED, [])
                continue

            if stack is None:
                stack = builder.create_pulumi_stack()
            builder.install_npm_deps()

            deployer = AppDeployer(stack, region)
            api_url: str = deployer.configiure_and_deploy(builder.cfg)
            if api_url == "":
                appResults[path] = AppResult(path, Result.DEPLOYMENT_FAILED, [])
                continue

            test_runner = TestRunner(builder.directory, api_url, upgrade, disable_tests)
            path_result.add_test_results(test_runner.run())
            upgrade = True
        
        # Build the app with klotho's mainline version and configure the pulumi config
        app_built = builder.build_app(path, Builds.MAINLINE)
        log.info(f'{app_built} main is built')
        if not app_built:
            appResults[path] = AppResult(path, Result.COMPILATION_FAILED, [])
            continue
        if stack is None:
            stack = builder.create_pulumi_stack()
        builder.install_npm_deps()

        deployer = AppDeployer(stack, region)
        api_url: str = deployer.configiure_and_deploy(builder.cfg)
        if api_url == "":
            appResults[path] = AppResult(path, Result.DEPLOYMENT_FAILED, [])
            continue

        test_runner = TestRunner(builder.directory, api_url, upgrade, disable_tests)
        path_result: AppResult = appResults[path]
        path_result.add_test_results(test_runner.run())

    for i in range(0,5):
        try:
            stack.destroy(on_output=print)
            result: subprocess.CompletedProcess[bytes] = subprocess.run(["pulumi", "stack", "rm", stack.name])
            result.check_returncode()
        except:
            stack.refresh()
    print(appResults)


if __name__ == '__main__':
    run()
