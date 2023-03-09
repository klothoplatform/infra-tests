import subprocess
import os
from pulumi import automation as auto
from enum import Enum
import logging
from app_util.config import TestConfig
import shutil
import tempfile
from urllib import request

log = logging.getLogger("DeploymentRunner")


class Builds(Enum):
    RELEASE = "release"
    MAINLINE = "main"

class AppBuilder:
    def __init__(self, directory: str, provider: str, run_id: str):
        self.app_name = os.path.split(directory)[-1]
        self.klotho_app_name = f'{directory}-{run_id}'
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
        log.info(f'Building application, {self.klotho_app_name}, with build {build} and config path {config_path}')
        tmp_path = None
        try:
            if build is Builds.RELEASE:
                klotho_bin_path = "./klotho_release"
                if not os.path.exists(klotho_bin_path):
                    with tempfile.NamedTemporaryFile(mode='x', delete=False) as f:
                        tmp_path = f.name
                    log.info(f'{klotho_bin_path} not found; downloading release klotho to {tmp_path}')
                    uname = os.uname()
                    if uname.sysname == 'Darwin':
                        release_url = f'http://srv.klo.dev/update/latest/darwin/{uname.machine}?stream=pro:latest'
                    elif uname.sysname == 'Linux':
                        release_url = 'http://srv.klo.dev/update/latest/linux/x86_64?stream=pro:latest'
                    else:
                        raise Exception(f"unsupported os: {uname.sysname}")
                    request.urlretrieve(release_url, tmp_path)
                    os.chmod(tmp_path, 0o755)
                    klotho_bin_path = tmp_path
            else:
                klotho_bin_path = "./klotho_main"

            if not os.path.exists(klotho_bin_path):
                raise Exception(f"Couldn't find klotho binary at {klotho_bin_path}")

            result: subprocess.CompletedProcess[bytes] = subprocess.run([klotho_bin_path, self.directory, "--app",
                                                                         self.klotho_app_name, "--provider",
                                                                         self.provider, "--config", config_path,
                                                                         "--outDir", self.output_dir])
            result.check_returncode()

            log.info(f'Successfully built {build} release for path {config_path}')
            self.install_npm_deps()
            self.copy_secrets()
            return True
        except Exception as e:
            log.error(e)
            return False
        finally:
            if tmp_path:
                log.info(f"Deleting {tmp_path}")
                os.remove(tmp_path)

        
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
