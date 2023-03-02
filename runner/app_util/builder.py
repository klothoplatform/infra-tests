import subprocess
import os
from pulumi import automation as auto
from enum import Enum
import logging
import shortuuid
from app_util.config import TestConfig
import shutil

log = logging.getLogger("DeploymentRunner")


class Builds(Enum):
    RELEASE = "release"
    MAINLINE = "main"

class AppBuilder:
    def __init__(self, directory: str, provider: str):
        self.app_name = os.path.split(directory)[-1]
        self.klotho_app_name = f'{directory}-{shortuuid.ShortUUID().random(length=6).lower()}'
        self.directory = os.path.join("apps", directory)
        self.provider = provider
        self.output_dir = os.path.join(self.directory, "compiled")

        if directory.startswith("ts"):
            result: subprocess.CompletedProcess[bytes] = subprocess.run(["npm", "install", "--prefix", self.directory], stdout=open(os.devnull, 'wb'))
            result.check_returncode()
            command = f'cd {self.directory}; npx tsc'
            result: subprocess.CompletedProcess[bytes] = subprocess.run(command, capture_output=True, shell=True)
            result.check_returncode()

        self.cfg = self.get_test_config()

    def build_app(self, config_path, build: Builds) -> bool:
        logging.log(1, f'Building application with build {build}')
        try:
            if build is Builds.RELEASE:
                result: subprocess.CompletedProcess[bytes] = subprocess.run(["./klotho_release", self.directory, "--app", 
                                                                        self.klotho_app_name, "--provider", 
                                                                        self.provider, "--config", config_path,
                                                                        "--outDir", self.output_dir])
                result.check_returncode()
            else:
                result: subprocess.CompletedProcess[bytes] = subprocess.run(["./klotho_main", self.directory, "--app", 
                                                                        self.klotho_app_name, "--provider", 
                                                                        self.provider, "--config", config_path,
                                                                        "--outDir", self.output_dir])
                result.check_returncode()
        except subprocess.CalledProcessError as e:
            print(e)
            return False
        log.info(f'Successfully built {build} release for path {config_path}')
        self.copy_secrets()
        return True

        
    def create_pulumi_stack(self) -> auto.Stack:
        stack = auto.create_stack(self.klotho_app_name, work_dir=self.output_dir)
        log.info(f'Successfully created stack for {self.klotho_app_name}')
        return stack

    def install_npm_deps(self):
        result: subprocess.CompletedProcess[bytes] = subprocess.run(["npm", "install", "--prefix", self.output_dir], stdout=open(os.devnull, 'wb'))
        result.check_returncode()


    def get_test_config(self) -> TestConfig:
        cfg = TestConfig(os.path.join(self.directory, "test-config.yaml"), self.klotho_app_name)
        cfg.read_config()
        return cfg
    
    def copy_secrets(self):
        for secret in self.cfg.secrets:
            output_path = os.path.join(self.output_dir, secret)
            dir = os.path.dirname(output_path)
            if not os.path.exists(dir):
                os.makedirs(dir)
            shutil.copy2(os.path.join(self.directory, secret), output_path)
        log.info(f'Successfully copied secrets for path')