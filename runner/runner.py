import click
import pulumi
from pulumi import automation as auto
from app_util.builder import AppBuilder, Builds
from app_util.deployer import AppDeployer
from test_runner import TestRunner
import concurrent.futures
import os
from util.result import AppResult, Result
from util.logging import log, PulumiLogging
import subprocess
import shortuuid

@click.command()
@click.option('--directories', type=str, required=True, help='The directories to be compiled')
@click.option('--region', type=str, required=True, help='The region to deploy to')
@click.option('--disable-tests', multiple=True, help='The tests to be disabled')
@click.option('--provider', type=str, required=True, help='The provider to test')
def run(directories, region, disable_tests, provider):
    run_id = shortuuid.ShortUUID.random(length=8)
    log.info(f'Starting run with id: {run_id}')
    # pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    appResults = {}
    for directory in directories.split(","):
        run_single(directory, region, disable_tests, provider, appResults, run_id)
    #     pool.submit(run_single(directory, region, disable_tests, provider, appResults))
    # pool.shutdown(wait=True)

    print(appResults)


def run_single(directory, region, disable_tests, provider, appResults, run_id):
    os.environ['PULUMI_CONFIG_PASSPHRASE'] = ""
    builder = AppBuilder(directory, provider)

    config_base_path = os.path.join("apps", directory, "config", provider)
    files: list[str] = os.listdir(config_base_path)
    upgrade = False
    stack: auto.Stack = None

    for file in files:
        path = os.path.join(config_base_path, file)
        if not os.path.isfile(path):
            log.debug(f'{path} is not a file. Skipping run.')
            continue

        pulumi_logger = PulumiLogging(run_id, path)

            # Build the app with klotho's released version and configure the pulumi config
<<<<<<< HEAD
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
=======
        stack = build_app(builder, path, appResults, upgrade, stack)
>>>>>>> 34ba86f (better logging)
        if stack is None:
            continue

        deployer = AppDeployer(stack, region, pulumi_logger)
        api_url: str = deployer.configiure_and_deploy(builder.cfg)
        if api_url == "":
            appResults[path] = AppResult(path, Result.DEPLOYMENT_FAILED, [])
            continue

        test_runner = TestRunner(builder.directory, api_url, upgrade, disable_tests)
        path_result: AppResult = appResults[path]
        path_result.add_test_results(test_runner.run())
        upgrade = True
        

    for i in range(0,5):
        try:
            stack.destroy(on_output=print)
            result: subprocess.CompletedProcess[bytes] = subprocess.run(["pulumi", "stack", "rm", stack.name])
            result.check_returncode()
        except:
            stack.refresh()


def build_app(builder: AppBuilder, path: str, appResults: dict, upgrade: bool, stack: auto.Stack) -> auto.Stack:
    build = Builds.RELEASE if not upgrade else Builds.MAINLINE
    app_built = builder.build_app(path, build)
    if not app_built:
        log.info(f'{path} {build} failed to build')
        appResults[path] = AppResult(path, Result.COMPILATION_FAILED, [])
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
