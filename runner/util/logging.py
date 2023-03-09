import logging
import os
import sys
from typing import List

log_directory = "logs"
pulumi_log_directory = "pulumi"
klotho_log_directory = "compilations"
service_log_directory = "service"

def configure_deployment_logger(run_id: str):
    log_path = os.path.join(log_directory, run_id)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    deployment_log = logging.getLogger("DeploymentRunner")
    deployment_log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - {%(pathname)s:%(lineno)d} - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    deployment_log.addHandler(handler)  
    fileHandler = logging.FileHandler(os.path.join(log_path, "stdout.txt"))
    fileHandler.setFormatter(formatter)
    deployment_log.addHandler(fileHandler)
    deployment_log.propagate = False

def configure_test_logger(run_id: str, app: str, config: str):
    app_log_path = os.path.join(log_directory, run_id, app, "test_output")
    if not os.path.exists(app_log_path):
        os.makedirs(app_log_path)
    test_log = logging.getLogger("TestRunner")
    remove_all_handlers(test_log)
    test_log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - {%(pathname)s:%(lineno)d} - %(levelname)s - %(message)s')
    fileHandler = logging.FileHandler(os.path.join(app_log_path, config))
    fileHandler.setFormatter(formatter)
    test_log.addHandler(fileHandler)
    test_log.propagate = False

def remove_all_handlers(logger: logging.Logger):
    for handler in logger.handlers:
        logger.removeHandler(handler)

class PulumiLogging:

    key_words = ["created", "updated", "failed", "deleted", "Previewing update", "View Live"]

    def __init__(self, run_id: str, app: str):
        self.base_path = os.path.join(log_directory, run_id, app, pulumi_log_directory)
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def log(self, msg: str):
        for word in self.key_words:
            if word in msg:
                print(msg)

        with open(self.current_path, "a") as log_file:
            log_file.write(msg+"\n")

    def set_file_name(self, file_name: str):
        self.current_path = os.path.join(self.base_path, file_name)

class ServiceLogging:
    key_words = ["created", "updated", "failed", "deleted", "Previewing update", "View Live"]

    def __init__(self, run_id: str, app: str, config: str):
        self.base_path = os.path.join(log_directory, run_id, app, service_log_directory, config)
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def write_file(self, file_name: str, contents: List[str]):
        with open(os.path.join(self.base_path, file_name), "a") as log_file:
            for line in contents:
                log_file.write(line+"\n")