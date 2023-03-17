from contextlib import contextmanager
import logging
import os
import sys
import threading
from typing import List, Literal

log_directory = "logs"
pulumi_log_directory = "pulumi"
klotho_log_directory = "compilations"
service_log_directory = "service"
thread_locals = threading.local()


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
    file_handler = logging.FileHandler(os.path.join(log_path, "stdout.txt"))
    file_handler.setFormatter(formatter)
    deployment_log.addHandler(file_handler)
    deployment_log.propagate = False


def configure_test_logger(run_id: str, app: str, config: str):
    app_log_path = os.path.join(log_directory, run_id, app, "test_output")
    if not os.path.exists(app_log_path):
        os.makedirs(app_log_path)
    test_log = logging.getLogger("TestRunner")
    remove_all_handlers(test_log)
    test_log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - {%(pathname)s:%(lineno)d} - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(os.path.join(app_log_path, config))
    file_handler.setFormatter(formatter)
    test_log.addHandler(file_handler)
    test_log.propagate = False


def remove_all_handlers(logger: logging.Logger):
    for handler in logger.handlers:
        logger.removeHandler(handler)


def is_github() -> bool:
    # GITHUB_ACTIONS is "true" when running in an action
    return bool(os.environ.get('GITHUB_ACTIONS'))


def log_milestone(level: Literal['notice', 'warning', 'error'], title: str, message: str):
    if is_github():
        print(f'::{level} title={title}::{message}')
    else:
        msg = ''
        if level != 'notice':
            msg = f'level.upper(): '
        msg += message


@contextmanager
def grouped_logging(title: str):
    # GH doesn't support hierarchical, sub-groupings of grouped logs. So instead, we'll use " ❱ " to set up the
    # breadcrumbs ourselves:
    # - If there's already a grouped_logging() open, close write "::endgroup::" to close it
    # - Then, print a "::group::..." that includes the full path of grouped_logging()s
    # - Finally, close the "::endgroup:: if this is the root level (otherwise, someone already closed it above)
    if not hasattr(thread_locals, "grouped_logs"):
        # grouped_logs is (str, bool) where the str is the title, and the bool is whether we still need to close it
        # The bool always starts out as true
        thread_locals.grouped_logs = []

    if is_github() and thread_locals.grouped_logs:
        print('::endgroup::')
        thread_locals.grouped_logs[-1] = (thread_locals.grouped_logs[-1][0], False)  # doesn't need closing anymore

    thread_locals.grouped_logs.append((title, True))
    prefix = '::group::' if is_github() else '### '
    print(f'{prefix}{" ❱ ".join([title for (title, closed) in thread_locals.grouped_logs])}')

    yield

    if is_github():
        _, needs_closing = thread_locals.grouped_logs.pop()
        if needs_closing:
            print('::endgroup::')


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
