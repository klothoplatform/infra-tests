import logging
import os

log = logging.getLogger("DeploymentRunner")
logging.basicConfig()

log_directory = "logs"
pulumi_log_directory = "pulumi"
klotho_log_directory = "compilations"

def sanitize_path_to_filename(path: str) -> str:
    return path.replace("/", "_") + ".txt"

class PulumiLogging:

    key_words = ["created", "updated", "failed", "deleted"]

    def __init__(self, run_id: str, app_and_config: str):
        self.path = os.path.join(log_directory, run_id, pulumi_log_directory, sanitize_path_to_filename(app_and_config))
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def log(self, msg: str):
        if any([word in self.key_words for word in msg]):
            print(msg)
        with open(self.path, "a") as log_file:
            log_file.write(msg)
