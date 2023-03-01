from ..util.result import TestResult, Result
from typing import List

class TestRunner:
    def __init__(self, api_endpoint, upgrade_path, disable_tests):
        self.api_endpoint = api_endpoint
        self.upgrade_path = upgrade_path
        self.disable_tests = disable_tests

    def run(self) -> List[TestResult]:
        result: List[TestResult] = [TestResult("Fake Test", Result.SUCCESS, "Hardcoded")]
        return result