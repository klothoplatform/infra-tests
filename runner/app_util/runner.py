import logging
import re
import time
from typing import Tuple, List

from pulumi import automation as auto

from app_util.builder import AppBuilder
from app_util.deployer import AppDeployer
from test_runner import TestRunner
from util.result import TestResult, Builds, Result
from util.logging import ServiceLogging, grouped_logging

log = logging.getLogger("DeploymentRunner")


class AppRunner:
    def __init__(self, builder: AppBuilder, deployer: AppDeployer):
        self.builder = builder
        self.deployer = deployer

    def deploy_and_test(self, run_id: str, path: str, build: Builds, upgrade_tests: bool, stack: auto.Stack) -> Tuple[auto.Stack, Result, List[TestResult]]:
        with grouped_logging(f'{build.name} on {path}{" (upgrade)" if upgrade_tests else ""}'):
            return self._deploy_and_test(run_id, path, build, upgrade_tests, stack)

    def _deploy_and_test(self, run_id: str, path: str, build, upgrade_tests: bool, stack: auto.Stack) -> Tuple[auto.Stack, Result, List[TestResult]]:
        builder = self.builder
        deployer = self.deployer
        sleep_time = 300 if stack is None else 30

        with grouped_logging(f'Building release application for path {path}'):
            # Build the app with klotho's released version and configure the pulumi config
            app_built = builder.build_app(path, build)
            if not app_built:
                return [stack, Result.COMPILATION_FAILED, None]

        if stack is None:
            with grouped_logging("Create Pulumi stack"):
                stack = builder.create_pulumi_stack()
                deployer.set_stack(stack)

        log.info(f'Configuring and deploying app {builder.cfg.app_name}')

        outputs: dict[str, str] = deployer.configure_and_deploy(builder.cfg)
        api_url = outputs.get("api_url", "")
        if api_url == "":
            return [stack, Result.DEPLOYMENT_FAILED, None]

        log.info(f'Sleeping for {sleep_time} seconds while stack settles.')
        time.sleep(sleep_time)

        with grouped_logging("Run tests"):
            outputs["api_url"] = format_url(api_url)
            test_runner = TestRunner(builder.app_name, outputs, upgrade_tests, [])
            test_results = test_runner.run()
            final_result = Result.SUCCESS
            for test_result in test_results:
                log.info(f'Test result for {builder.klotho_app_name}: {test_result.to_string()}')
                if test_result.result != Result.SUCCESS:
                    final_result = Result.TESTS_FAILED

        with grouped_logging("Download logs"):
            service_logger = ServiceLogging(run_id, builder.app_name, path.split("/")[-1])
            deployer.download_logs(service_logger)

        return [stack, final_result, test_results]


def format_url(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'http://{}'.format(url)
    return url
