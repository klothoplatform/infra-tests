import subprocess
from pulumi import automation as auto
from app_util.config import TestConfig
from util.logging import PulumiLogging, ServiceLogging, grouped_logging
import logging
import os
import boto3

log = logging.getLogger("DeploymentRunner")

class AppDeployer:
    def __init__(self, region: str, pulumi_logger: PulumiLogging):
        self.region = region
        self.pulumi_logger = pulumi_logger
        self.logs_client= boto3.client('logs', region_name=self.region)


    def set_stack(self, stack: auto.Stack):
        self.stack = stack

    def configure_and_deploy(self, cfg: TestConfig) -> str:
        with grouped_logging("Configuring stack"):
            self.configure_tags()
            self.configure_region()
            self.configure_pulumi_app(cfg)
        for i in range(0,5):
            with grouped_logging(f'Previewing stack {self.stack.name}, attempt #{i}'):
                try:
                    self.stack.preview(on_output=self.pulumi_logger.log)
                    break
                except Exception as e:
                    log.error(f'Failed to preview stack', exc_info=True)
                    if i == 4:
                        return ""
        for i in range(0, 5):
            try:
                with grouped_logging(f'Deploying stack {self.stack.name} to region {self.region}, attempt #{i}'):
                    url = self.deploy_app()
                    log.info(f'Deployed stack, {self.stack.name}, successfully. Got API Url: {url}')
                    return url
            except Exception as e:
                with grouped_logging(f'Deployment of stack, {self.stack.name}, failed.'):
                    log.error(f'Deployment of stack, {self.stack.name}, failed.', exc_info=True)
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

    def configure_tags(self):
        result: subprocess.CompletedProcess[bytes] = subprocess.run(
            ["pulumi", "stack", "tag", "set", "usage", "infra-test", "-s", self.stack.name],
            stdout=open(os.devnull, 'wb'),
            cwd=self.stack.workspace.work_dir
        )
        result.check_returncode()

    def configure_region(self):
        self.stack.set_config("aws:region", auto.ConfigValue(self.region))

    def configure_pulumi_app(self, cfg: TestConfig):
        for key in cfg.pulumi_config:
            self.stack.set_config(f'{cfg.app_name}:{key}', auto.ConfigValue(cfg.pulumi_config[key]))

    def destroy_and_remove_stack(self, output_dir: str) -> bool:
         for i in range(0,5):
            try:
                with grouped_logging(f'Destroying stack {self.stack.name}, attempt #{i}'):
                    self.pulumi_logger.set_file_name(f'destroy.txt')
                    self.stack.destroy(on_output=self.pulumi_logger.log)
                    log.info(f'Removing stack {self.stack.name}')
                    command = f'cd {output_dir}; pulumi stack rm -s {self.stack.name} -y'
                    result: subprocess.CompletedProcess[bytes] = subprocess.run(command, capture_output=True, shell=True)
                    result.check_returncode()
                    return True
            except Exception as e:
                with grouped_logging("Destroy failed"):
                    log.error(e)
                    log.info(f'Refreshing stack {self.stack.name}')
                    self.stack.refresh()
                    return False
            
    def download_logs(self, logger: ServiceLogging):
        deployment = self.stack.export_stack()
        resources = deployment.deployment.get('resources')
        for resource in resources:
            
            # This covers lambda and ecs since we explicitly create the log groups for both
            if resource['type'] == 'aws:cloudwatch/logGroup:LogGroup':
                log_group_name: str = resource['outputs']['name']
                log.info(f'Getting logs from {log_group_name}')
                log_streams = self.logs_client.describe_log_streams(
                    logGroupName=log_group_name,
                    limit=50
                )
                for stream in log_streams['logStreams']:
                    stream_name: str = stream['logStreamName']
                    events = self.get_log_events(log_group_name, stream_name)
                    logger.write_file(f'{log_group_name.replace("/", "_")}-{stream_name.replace("/", "_")}', events)

            elif resource['type'] == 'aws:eks/cluster:Cluster':
                cluster_name = resource['outputs']['name']
                log_group_name: str = f'/aws/containerinsights/{cluster_name}/application'
                log.info(f'Getting logs from {log_group_name}')
                log_streams = self.logs_client.describe_log_streams(
                    logGroupName=log_group_name,
                    limit=50
                )
                for stream in log_streams['logStreams']:
                    stream_name: str = stream['logStreamName']
                    events = self.get_log_events(log_group_name, stream_name)
                    logger.write_file(stream_name.replace("/", "_"), events)
                    

    def get_log_events(self, log_group_name: str, stream: str):
        kwargs = {
            'logGroupName': log_group_name,
            'limit': 50,
            'logStreamName': stream
        }
        events = []
        while True:
            resp = self.logs_client.get_log_events(**kwargs)
            try:
                [events.append(e['message']) for e in resp['events']]
                kwargs['nextToken'] = resp['nextToken']
            except KeyError:
                break
        return events
