from typing import List

import yaml


class TestConfig:
    def __init__(self, path, app_name):
        self.path = path
        self.pulumi_config = {str: str}
        self.secrets = List[str]
        self.app_name = app_name
        self.gateway_name: str | None = None
        self.static_unit_name: str | None = None

    def read_config(self):
        with open(self.path, "r") as stream:
            try:
                cfg = yaml.safe_load(stream)
                default_cfg = cfg["default"]
                self.pulumi_config = default_cfg["pulumi-config"]
                self.secrets = default_cfg["secrets"]
                self.gateway_name = default_cfg["gateway-name"]
                self.static_unit_name = default_cfg["static-unit-name"]
            except yaml.YAMLError as exc:
                print(exc)
