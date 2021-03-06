"""
AUTHOR: Matt Durrant

This module contains a RunSubprocessStepSuper subclass called RunSamtools.

This just checks to see that samtools is the correct version.
"""

import subprocess
from mod.config.custom import SamtoolsCustomConfig
from mod.config.fixed import SamtoolsFixedConfig
from mod.subprocess_step_superclass import RunSubprocessStepSuper


class RunSamtools(RunSubprocessStepSuper):
    def __init__(self, logger=None):
        custom_config = SamtoolsCustomConfig()
        fixed_config = SamtoolsFixedConfig()

        name = fixed_config.name
        output_dir = None
        execution_path = custom_config.execution_path

        version = custom_config.version
        version_flag = custom_config.version_flag
        version_parser = fixed_config.version_parser

        input_file = fixed_config.input_file
        output_file = fixed_config.output_file

        args = custom_config.args

        log_name = fixed_config.log_name
        logger = logger

        super().__init__(name=name, output_dir=output_dir, execution_path=execution_path, version=version,
                         version_flag=version_flag, version_parser=version_parser, input_file=input_file,
                         output_file=output_file, args=args, log_name=log_name, logger=logger)

    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parse=False):
        super().check_version(stderr=subprocess.STDOUT, ignore_error=True)

    def run(self, make_output_dir=True):
        self.check_version()

    def execute_command(self, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False):
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
