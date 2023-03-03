import subprocess
from pulumi import automation as auto
from app_util.config import TestConfig
from util.logging import PulumiLogging
import logging

log = logging.getLogger("DeploymentRunner")

class AppDeployer:
    def __init__(self, region: str, pulumi_logger: PulumiLogging):
        self.region = region
        self.pulumi_logger = pulumi_logger

    def set_stack(self, stack: auto.Stack):
        self.stack = stack

    def configiure_and_deploy(self, cfg: TestConfig) -> str:
        self.configure_region()
        self.configure_pulumi_app(cfg)
        try:
            log.info(f'Previewing stack {self.stack.name}')
            self.stack.preview(on_output=self.pulumi_logger.log)
        except Exception as e:
            log.error(e)
            return ""
        for i in range(0,5):
            try:
                log.info(f'Deploying stack {self.stack.name}')
                url = self.deploy_app()
                log.info(f'Deployed stack, {self.stack.name}, successfully. Got API Url: {url}')
                return url
            except Exception as e:
                log.error(f'Deployment of stack, {self.stack.name}, failed.')
                log.info(f'Refreshing stack {self.stack.name}')
                self.stack.refresh()
        return ""

    # deploy_app deploys the stack and returns the first apiUrl expecting it to be the intended endpoint for tests
    def deploy_app(self) -> str:
        result: auto.UpResult = self.stack.up(on_output=self.pulumi_logger.log)
        output: auto.OutputMap = result.outputs
        value: auto.OutputValue = output.get("apiUrls")
        if len(value.value) > 0:
            if type(value.value[0]) is str:
                return value.value[0]
        return ""

    def configure_region(self):
        self.stack.set_config("aws:region", auto.ConfigValue(self.region))

    def configure_pulumi_app(self, cfg: TestConfig):
        for key in cfg.pulumi_config:
            self.stack.set_config(f'{cfg.app_name}:{key}', auto.ConfigValue(cfg.pulumi_config[key]))

    def destroy_and_remove_stack(self, output_dir: str) -> bool:
         for i in range(0,5):
            try:
                log.info(f'Destroying stack {self.stack.name}')
                self.pulumi_logger.set_file_name(f'destroy.txt')
                self.stack.destroy(on_output=self.pulumi_logger.log)
                log.info(f'Removing stack {self.stack.name}')
                command = f'cd {output_dir}; pulumi stack rm -s {self.stack.name} -y'
                result: subprocess.CompletedProcess[bytes] = subprocess.run(command, capture_output=True, shell=True)
                log.info(result.stdout)
                result.check_returncode()
                return True
            except Exception as e:
                log.error(e)
                log.info(f'Refreshing stack {self.stack.name}')
                self.stack.refresh()
            finally:
                return False