from enum import Enum
from typing import List
from app_util.builder import Builds
from junitparser import TestSuite


class Result(Enum):
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    TESTS_FAILED = "TESTS_FAILED"
    COMPILATION_FAILED = "COMPILATION_FAILED"
    DEPLOYMENT_FAILED = "DEPLOYMENT_FAILED"
    DESTROY_FAILED = "DESTROY_FAILED"


class TestResult:
    def __init__(self, name: str, result: Result, reason: str, reports: list[TestSuite]):
        self.name = name
        self.result = result
        self.reason = reason
        self.reports = reports

    def to_string(self) -> str:
        return f'name: {self.name}\n\tresult: {self.result}\n\reason: {self.reason}'


def sanitize_result_key(key: str) -> str:
    return key.replace('/','_').replace('.','-')


class AppResult:
    def __init__(self, directory: str, build: Builds, result: Result, test_results: List[TestResult], step: int):
        self.result = result
        self.build = build
        self.directory = directory
        self.test_results = test_results
        self.step = step

    def set_result(self, result: Result):
        self.result = result

    def add_test_results(self, test_results: List[TestResult]):
        did_any_test_fail = False
        for result in test_results:
            self.test_results.append(result)
            if result.result is not Result.SUCCESS:
                self.result = Result.TESTS_FAILED
                did_any_test_fail = True

        if self.result is Result.STARTED and not did_any_test_fail:
            self.result = Result.SUCCESS

    def to_string(self) -> str:
        return f'directory: {self.directory}, build: {self.build}\n\tstep: {self.step}, result: {self.result}\n'
