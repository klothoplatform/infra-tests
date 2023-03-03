
from app_util.builder import AppBuilder
from app_util.deployer import AppDeployer
from util.result import TestResult, Builds, Result
from test_runner import TestRunner
import logging
from pulumi import automation as auto
from typing import Tuple, List
from urllib.parse import urlparse, urlunparse

import re

def formaturl(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'http://{}'.format(url)
    return url

log = logging.getLogger("DeploymentRunner")

class AppRunner:
    def __init__(self, builder: AppBuilder, deployer: AppDeployer):
        self.builder = builder
        self.deployer = deployer

    def deploy_and_test(self, path: str, upgrade: bool, stack) -> Tuple[auto.Stack, Result, List[TestResult]]:
        builder = self.builder
        deployer = self.deployer
        build = Builds.RELEASE if not upgrade else Builds.MAINLINE

        log.info(f'Building release application for path {path}')
        # Build the app with klotho's released version and configure the pulumi config
        app_built = builder.build_app(path, build)
        if not app_built:
            return [None, Result.COMPILATION_FAILED, None]

        if stack is None:
            stack = builder.create_pulumi_stack()
            deployer.set_stack(stack)

        log.info(f'Configuring and deploying app {builder.cfg.app_name}')

        api_url: str = deployer.configiure_and_deploy(builder.cfg)
        if api_url == "":
            return [stack, Result.COMPILATION_FAILED, None]

        url = formaturl(api_url)
        parsed_url = urlparse(url, 'https')

        test_runner = TestRunner(builder.app_name, urlunparse([parsed_url.scheme,parsed_url.netloc,'','','','']), parsed_url.path, upgrade, [])
        test_results = test_runner.run()
        final_result = Result.SUCCESS
        for test_result in test_results:
            log.info(test_result.to_string())
            if test_result.result != Result.SUCCESS:
                final_result = Result.TESTS_FAILED

        return [stack, final_result, test_results]