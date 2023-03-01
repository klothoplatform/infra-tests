import subprocess
import os
from pulumi import automation as auto
from enum import Enum

class Builds(Enum):
    RELEASE = "release"
    MAINLINE = "main"

class AppBuilder:
    def __init__(self, directory: str, provider: str):
        self.app_name = directory
        self.directory = directory
        self.provider = provider

    def build_app(self, config_path, build: Builds) -> bool:
        try:
            if build is Builds.RELEASE:
                result: subprocess.CompletedProcess[bytes] = subprocess.run(["klotho_release", self.directory, "--app", 
                                                                        self.app_name, "--provider", 
                                                                        self.provider, "--config", config_path])
                result.check_returncode()
                return True
            else:
                result: subprocess.CompletedProcess[bytes] = subprocess.run(["klotho_main", self.directory, "--app", 
                                                                        self.app_name, "--provider", 
                                                                        self.provider, "--config", config_path])
                result.check_returncode()
                return True
        except subprocess.CalledProcessError as e:
            print(e)
            return False
        
    def create_pulumi_stack(self) -> auto.Stack:
        stack = auto.create_stack(self.app_name, work_dir=os.path.join(".",self.directory, "compiled"))
        return stack
