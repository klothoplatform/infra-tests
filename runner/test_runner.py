import logging
import os
import re
import subprocess

from util.result import TestResult, Result

log = logging.getLogger("TestRunner")


class TestRunner:
    def __init__(self, app_name, api_endpoint, upgrade_path, disable_tests, provider="aws"):
        self.app_name: str = app_name
        self.api_endpoint: str = api_endpoint
        self.upgrade_path: bool = upgrade_path
        self.disable_tests: str = disable_tests if disable_tests is not None else ""
        self.provider = "unknown" if provider is None else provider

    def run(self) -> list[TestResult]:
        log.info(f'Running tests for {self.app_name} and is upgrade={self.upgrade_path}')
        log.info(f'Targeting endpoint {self.api_endpoint}')
        log.info(f'Disabled tests: {self.disable_tests}')
        command = " ".join([
            "cd integ-tests;",
            f'API_URL="{self.api_endpoint}"',
            f'APP_NAME="{self.app_name}"',
            f'PROVIDER="{self.provider}"',
            f'PYTHONPATH="{os.path.abspath(os.path.join(os.curdir, "integ-tests"))}"',
            "pytest"
        ])

        upgrade_marker = "not post_upgrade" if self.upgrade_path is False else "not pre_upgrade"
        disable_tests = f"--ignore '{self.disable_tests}'" if self.disable_tests != "" else ""
        app_marker = re.sub("[\\s-]", "_", self.app_name.lower())
        markers = app_marker
        markers = add_marker_subexpression(markers, upgrade_marker)
        log.info(f'Running with markers {markers}')
        args = [command, "-m", f'"{markers}"', disable_tests]
        log.info(" ".join(args))
        result: subprocess.CompletedProcess[bytes] = subprocess.run(" ".join(args), capture_output=True, shell=True, text=True)

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


def add_marker_subexpression(markers: str, subexpr: str) -> str:
    if subexpr is not None and subexpr != "":
        return f"{markers} and ({subexpr})"
    return markers
