import click
import pulumi
from pulumi import automation as auto
from builder import AppBuilder, Builds
from deployer import AppDeployer
from util.result import AppResult, Result
from test_runner.runner import TestRunner
import concurrent.futures
import os

@click.command()
@click.option('--directories', type=str, help='The directories to be compiled')
@click.option('--region', type=str, help='The region to deploy to')
@click.option('--disable-tests', multiple=True, help='The tests to be disabled')
def run(directories, region, disable_test):
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    appResults = dict[str: AppResult]
    for directory in directories.split(","):
        pool.submit(run_single(directory, region, disable_test, appResults))
    pool.shutdown(wait=True)


def run_single(directory, region, disable_tests, appResults):
    builder = AppBuilder(directory, "aws")
    files: list[str] = os.listdir(os.path.join(".",directory, "config"))
    upgraded = False

    for path in files:
        if not os.path.isfile(path):
            continue

        if not upgraded:
            # Build the app with klotho's released version and configure the pulumi config
            app_built = builder.build_app(path, Builds.RELEASE)
            if not app_built:
                appResults[directory] = AppResult(directory, Result.COMPILATION_FAILED, [])
                continue
            stack = builder.create_pulumi_stack()

            deployer = AppDeployer(stack, region)
            api_url: str = deployer.configiure_and_deploy()


            test_runner = TestRunner(api_url, upgraded, disable_tests)
            test_runner.run()
        
        # Build the app with klotho's mainline version and configure the pulumi config
        app_built = builder.build_app(path, Builds.MAINLINE)
        if not app_built:
            appResults[directory] = AppResult(directory, Result.COMPILATION_FAILED, [])
            continue
        stack = builder.create_pulumi_stack()

        deployer = AppDeployer(stack, region)
        api_url: str = deployer.configiure_and_deploy()

        test_runner = TestRunner(api_url, upgraded, disable_tests)
        test_runner.run()


if __name__ == '__main__':
    run()
