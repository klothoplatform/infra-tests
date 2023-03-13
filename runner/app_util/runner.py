import logging
import re
import time
from typing import Tuple, List

from pulumi import automation as auto

from app_util.builder import AppBuilder
from app_util.deployer import AppDeployer
from test_runner import TestRunner
from util.result import TestResult, Builds, Result
from util.logging import ServiceLogging

log = logging.getLogger("DeploymentRunner")


class AppRunner:
    def __init__(self, builder: AppBuilder, deployer: AppDeployer):
        self.builder = builder
        self.deployer = deployer

    def deploy_and_test(self, run_id: str, path: str, upgrade: bool, stack: auto.Stack) -> Tuple[auto.Stack, Result, List[TestResult]]:
        builder = self.builder
        deployer = self.deployer
        build = Builds.RELEASE if not upgrade else Builds.MAINLINE
        sleep_time = 300 if stack is None else 30

        log.info(f'Building release application for path {path}')
        # Build the app with klotho's released version and configure the pulumi config
        app_built = builder.build_app(path, build)
        if not app_built:
            return [stack, Result.COMPILATION_FAILED, None]

        if stack is None:
            stack = builder.create_pulumi_stack()
            deployer.set_stack(stack)

        log.info(f'Configuring and deploying app {builder.cfg.app_name}')

        api_url: str = deployer.configure_and_deploy(builder.cfg)
        if api_url == "":
            return [stack, Result.COMPILATION_FAILED, None]

        url = format_url(api_url)

        log.info(f'Sleeping for {sleep_time} seconds while stack settles.')
        time.sleep(sleep_time)

        test_runner = TestRunner(builder.app_name, url, upgrade, [])
        test_results = test_runner.run()
        final_result = Result.SUCCESS
        for test_result in test_results:
            log.info(f'Test result for {builder.klotho_app_name}: {test_result.to_string()}')
            if test_result.result != Result.SUCCESS:
                final_result = Result.TESTS_FAILED


        service_logger = ServiceLogging(run_id, builder.app_name, path.split("/")[-1])
        deployer.download_logs(service_logger)

        return [stack, final_result, test_results]


def format_url(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'http://{}'.format(url)
    return url
