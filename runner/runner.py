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
from junitparser import TestCase
import re


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
    app_results: dict[str, AppResult] = {}
    for directory in directories.split(","):
        run_single(directory, region, provider, app_results, run_id, config_files, no_destroy)
    #     pool.submit(run_single(directory, region, disable_tests, provider, app_results))
    # pool.shutdown(wait=True)

    for key, result in app_results.items():
        if result.result != Result.SUCCESS:
            result_code = 1
        log.info(f'Result for {key}: {result.result.value}')

        for test_result in (result.test_results or []):
            for report in test_result.reports:
                test_case: TestCase
                for test_case in report:
                    _print_test_case_failure(test_case)

    exit(result_code)


def run_single(directory: str, region: str, provider: str, app_results: dict[str, AppResult], run_id: str, config_filenames: List[str], no_destroy: bool):
    try:
        os.environ['PULUMI_CONFIG_PASSPHRASE'] = ""
        builder = AppBuilder(directory, provider, run_id)
        pulumi_logger = PulumiLogging(run_id, builder.app_name)
        deployer = AppDeployer(region, pulumi_logger)
        app_runner = AppRunner(builder, deployer)

        config_base_path = os.path.join("apps", directory, "config", provider)
        files: list[str] = os.listdir(config_base_path)
        files.sort()

        upgrade_path = False
        stack: auto.Stack = None
        step = 1
        try:
            for file in files:
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
                    stack, result, test_results = app_runner.deploy_and_test(run_id, path, Builds.RELEASE, upgrade_tests, stack)
                    app_results.update({result_key: AppResult(path, Builds.RELEASE, result, test_results, step)})
                    step += 1
                    upgrade_tests = True
                    upgrade_path = True
                    
                # Build the app with klotho's mainline version and configure the pulumi config
                result_key = sanitize_result_key(f'{path}-{Builds.MAINLINE}')
                stack, result, test_results = app_runner.deploy_and_test(run_id, path, Builds.MAINLINE, upgrade_tests, stack)
                app_results.update({result_key: AppResult(path, Builds.MAINLINE, result, test_results, step)})
                step += 1

        except Exception as e:
            log.error(e)
            log.error(traceback.print_exc())
            app_results.update({path: AppResult(path, None, result, test_results, step)})
            step += 1
        finally:
            if stack is not None and not no_destroy:
                deploy_succeeded = deployer.destroy_and_remove_stack(builder.output_dir)
                result = Result.SUCCESS if deploy_succeeded else Result.DESTROY_FAILED
                result_key = sanitize_result_key(f'{stack.name}-destroy')
                app_results.update({result_key: AppResult(path, None, Result.FAILED, [], step)})
    except Exception as e:
        log.error(f'Failed to configure app  run {e}')
        log.error(traceback.print_exc())
        app_results.update({directory: AppResult(directory, None, Result.FAILED, [], 0)})


def _print_test_case_failure(test_case: TestCase):
    if test_case.is_passed or test_case.is_skipped:
        return
    # The format of test_case.result[*].text is something like:
    # ╭──────────────────────────────────────────────╮
    # │    def test_whatever():                      │
    # │        some_test_code()                      │
    # │        blah_blah() # potentially a lot here! │
    # │        blah_blah_blah()                      │
    # │>       assert "yes" == "no"                  │
    # │E       AssertionError: assert 'yes' == 'no'  │
    # │E         - no                                │
    # │E         + yes                               │
    # │                                              │
    # │test_file.py:6: AssertionError                │
    # ╰──────────────────────────────────────────────╯
    # We'll ignore everything until the ">", and then also ignore the blank line. Our final
    # output will be:
    # ╭──────────────────────────────────────────────╮
    # │FAILURE test_whatever:                        │
    # │>       assert "yes" == "no"                  │
    # │E       AssertionError: assert 'yes' == 'no'  │
    # │E         - no                                │
    # │E         + yes                               │
    # │test_file.py:6: AssertionError                │
    # ╰──────────────────────────────────────────────╯
    for tc_result in test_case.result:
        print(f'FAILURE: {test_case.name}:')
        result_line: str = ''
        should_output = False
        error_oneline: str = ''
        for result_line in tc_result.text.split('\n'):
            if not should_output:
                should_output = result_line.startswith(">")
            if (not error_oneline) and result_line.startswith("E"):
                error_oneline = result_line[1:].strip()
            if should_output and result_line.strip():
                print('│' + result_line)

        # GITHUB_ACTIONS is "true" when running in an action. In that case, print out an GH error command
        if os.environ.get('GITHUB_ACTIONS'):
            last_line_match = re.match('(?P<file>[^:]+):(?P<line>\\d+): (?P<message>.*)', result_line)
            if last_line_match:
                loc = last_line_match.groupdict()
                if error_oneline.startswith(loc["message"]):
                    # Common case: the message is "AssertionError", and oneline is "AssertionError: foo"
                    error_oneline = error_oneline[len(loc["message"]):]  # trim
                    error_oneline = error_oneline.lstrip(": ")
                print(f'::error file={loc["file"]},line={loc["line"]},title={loc["message"]} in {test_case.name}::{error_oneline}')
            else:
                if not error_oneline:
                    error_oneline = "error"
                print(f'::error title=Failure::{error_oneline}')

            
if __name__ == '__main__':
    run()
