import subprocess

from mod.pipeline.version_parsers import parse_java_version
from mod.pipeline.run_process.run_process_step_super import RunProcessStepSuper
from mod.pipeline.config.custom import JavaCustomConfig
from mod.pipeline.config.fixed import JavaFixedConfig

class RunJava(RunProcessStepSuper):

    def __init__(self, logger=None):
        custom_config = JavaCustomConfig()
        fixed_config = JavaFixedConfig()

        name = fixed_config.name
        output_dir = None
        execution_path = custom_config.execution_path

        version = custom_config.version
        version_flag = custom_config.version_flag
        version_parser = fixed_config.version_parser

        input = fixed_config.input
        output = fixed_config.output

        args = custom_config.args

        log_name = fixed_config.log_name
        logger = logger


        super().__init__(name=name, output_dir=output_dir, execution_path=execution_path, version=version,
                         version_flag=version_flag, version_parser=version_parser, input=input,
                         output=output, args=args, log_name=log_name, logger=logger)


    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parse=False):
        super().check_version(stderr=subprocess.STDOUT, ignore_error=True)

    def run(self):
        self.check_version()

    def execute_command(self):
        raise NotImplementedError

    def save_log(self):
        raise NotImplementedError

    def get_log_json(self):
        raise NotImplementedError

    def get_log_path(self):
        raise NotImplementedError

    def format_command(self):
        raise NotImplementedError


    def retrieve_output_path(self, default_output=True):
        raise NotImplementedError

