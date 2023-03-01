from enum import Enum
from typing import List
from app_util.builder import Builds

class Result(Enum):
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

class AppResult:
    def __init__(self, directory: str, build: Builds, result: Result):
        self.result = result
        self.build = build
        self.directory = directory
        self.test_results = []

    def add_test_results(self, test_results: List[TestResult]):
        self.test_results = test_results