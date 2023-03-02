import subprocess
from pprint import pprint
from typing import List
import logging
from util.result import TestResult, Result
import os

log = logging.getLogger("TestRunner")


class TestRunner:
    def __init__(self, app_name, api_endpoint, upgrade_path, disable_tests):
        self.app_name = app_name
        self.api_endpoint = api_endpoint
        self.upgrade_path = upgrade_path
        self.disable_tests = disable_tests if disable_tests is not None else ""

    def run(self) -> list[TestResult]:
        log.info(f'Running tests for {self.app_name} and is upgrade={self.upgrade_path}')
        log.info(f'Targeting endpoint {self.api_endpoint}')
        log.info(f'Disabled tests: {self.disable_tests}')
        command = f"""API_URL="{self.api_endpoint}" pytest"""
        upgrade = "-k 'not upgrade_path' " if self.upgrade_path is False else ""
        disable_tests = f"--ignore '{self.disable_tests}'" if self.disable_tests != "" else ""
        args = [command, "-x", f"'./integ-tests/{self.app_name}'", upgrade, disable_tests]
        print(" ".join(args))
        result: subprocess.CompletedProcess[bytes] = subprocess.run(args, capture_output=True, shell=True, text=True)

        status = None
        out = str(result.stdout)
        err = str(result.stderr)

        if len(out) > 0:
            log.info(out)
        if len(err) > 0:
            log.error(err)

        if result.returncode == 0:
            status = Result.SUCCESS
        elif result.returncode == 1 and out.endswith("======"):
            status = Result.TESTS_FAILED
        else:
            status = Result.FAILED
        return [TestResult(self.app_name, status, f"stdout:\n{out}\nstderr:{err}")]
