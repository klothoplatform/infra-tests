import logging
import os
import sys

log_directory = "logs"
pulumi_log_directory = "pulumi"
klotho_log_directory = "compilations"

def configureLoggers(run_id: str):
    log_path = os.path.join(log_directory, run_id)
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    deployment_log = logging.getLogger("DeploymentRunner")
    deployment_log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    deployment_log.addHandler(handler)  
    fileHandler = logging.FileHandler(os.path.join(log_path, "stdout.txt"))
    fileHandler.setFormatter(formatter)
    deployment_log.addHandler(fileHandler)
    deployment_log.propagate = False

    test_log = logging.getLogger("TestRunner")
    test_log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    test_log.addHandler(handler)  
    fileHandler = logging.FileHandler(os.path.join(log_path, "test_output.txt"))
    fileHandler.setFormatter(formatter)
    test_log.addHandler(fileHandler)
    test_log.propagate = False



class PulumiLogging:

    key_words = ["created", "updated", "failed", "deleted", "Previewing update", "View Live"]

    def __init__(self, run_id: str, app: str):
        self.path = os.path.join(log_directory, run_id, pulumi_log_directory, app)
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))

    def log(self, msg: str):
        for word in self.key_words:
            if word in msg:
                print(msg)

        with open(self.path, "a") as log_file:
            log_file.write(msg+"\n")

    def set_file_name(self, file_name: str):
        self.path = os.path.join(os.path.dirname(self.path), file_name)
