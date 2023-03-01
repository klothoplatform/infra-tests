import subprocess
from pulumi import automation as auto
from app_util.config import TestConfig
from util.logging import PulumiLogging

class AppDeployer:
    def __init__(self, stack: auto.Stack, region: str, pulumi_logger: PulumiLogging):
        self.stack = stack
        self.region = region
        self.pulumi_logger = pulumi_logger

    def configiure_and_deploy(self, cfg: TestConfig) -> str:
        self.configure_region()
        self.configure_pulumi_app(cfg)
        try:
            self.stack.preview(on_output=self.pulumi_logger.log)
        except:
            return ""
        for i in range(0,5):
            try:
                url = self.deploy_app()
                return url
            except Exception as e:
                print(e)
                self.stack.refresh()
        return ""

    # deploy_app deploys the stack and returns the first apiUrl expecting it to be the intended endpoint for tests
    def deploy_app(self) -> str:
        result: auto.UpResult = self.stack.up(on_output=self.pulumi_logger.log)
        output: auto.OutputMap = result.outputs
        output.get("apiUrls")[0]

    def configure_region(self):
        self.stack.set_config("aws:region", auto.ConfigValue(self.region))

    def configure_pulumi_app(self, cfg: TestConfig):
        for key in cfg.pulumi_config:
            self.stack.set_config(f'{cfg.app_name}:{key}', auto.ConfigValue(cfg.pulumi_config[key]))
