from enum import Enum
from typing import List
from ..deployment_runner.builder import Builds

class Result(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    TESTS_FAILED = "TESTS_FAILED"
    COMPILATION_FAILED = "COMPILATION_FAILED"

class TestResult:
    def __init__(self, name: str, result: Result, reason: str):
        self.name = name
        self.result = result
        self.reason = reason

class AppResult:
    def __init__(self, directory: str, build: Builds, result: Result, test_results: List[TestResult]):
        self.result = result
        self.build = build
        self.directory = directory
        self.test_results = test_results