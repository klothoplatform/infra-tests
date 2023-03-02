from enum import Enum
from typing import List
from app_util.builder import Builds

class Result(Enum):
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    TESTS_FAILED = "TESTS_FAILED"
    COMPILATION_FAILED = "COMPILATION_FAILED"
    DEPLOYMENT_FAILED = "DEPLOYMENT_FAILED"

class TestResult:
    def __init__(self, name: str, result: Result, reason: str):
        self.name = name
        self.result = result
        self.reason = reason

    def to_string(self):
        return f'name: {self.name}\n\tresult: {self.result}\n\reason: {self.reason}'


def sanitize_result_key(key: str) -> str:
    return key.replace('/','_').replace('.','-')

class AppResult:
    def __init__(self, directory: str, build: Builds, result: Result):
        self.result = result
        self.build = build
        self.directory = directory
        self.test_results = []

    def set_result(self, result: Result):
        self.result = result

    def add_test_results(self, test_results: List[TestResult]):
        for result in test_results:
            self.test_results.append(result)
            if result.result is not Result.SUCCESS:
                self.result = Result.TESTS_FAILED
            elif self.result is not Result.SUCCESS:
                self.result = Result.SUCCESS

    def to_string(self):
        string = f'directory: {self.directory}, build: {self.buid}\n\tresult: {self.result}\n'
        for result in self.test_results:
            string += f'{result.to_string}\n'