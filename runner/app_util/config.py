from typing import List
import yaml

class TestConfig:
    def __init__(self, path, app_name):
        self.path = path
        self.pulumi_config = {str: str}
        self.secrets = List[str]
        self.order = List[str]
        self.app_name = app_name

    def read_config(self):
        with open(self.path, "r") as stream:
            try:
                cfg = yaml.safe_load(stream)
                default_cfg = cfg["default"]
                self.pulumi_config = default_cfg["pulumi-config"]
                self.secrets = default_cfg["secrets"]
                self.order = default_cfg["run-order"]
            except yaml.YAMLError as exc:
                print(exc)
