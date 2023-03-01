import subprocess
from pulumi import automation as auto

class AppDeployer:
    def __init__(self, stack: auto.Stack, region: str):
        self.stack = stack
        self.region = region

    def configiure_and_deploy(self) -> str:
        self.configure_region()
        return self.deploy_app()

    # deploy_app deploys the stack and returns the first apiUrl expecting it to be the intended endpoint for tests
    def deploy_app(self) -> str:
        result: auto.UpResult = self.stack.up()
        output: auto.OutputMap = result.outputs
        output.get("apiUrls")[0]

    def configure_region(self):
        self.stack.set_config("aws:region", self.region)