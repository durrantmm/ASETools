"""
This module contains a RunSubprocessStepSuper subclass called RunSamtoolsIndex.

It executes the samtools index command using the subprocess standard library module.
"""

import subprocess
from os.path import dirname
from mod.config.custom import SamtoolsIndexCustomConfig
from mod.config.fixed import SamtoolsIndexFixedConfig
from mod.misc.string_constants import *
from mod.subprocess_step_superclass import RunSubprocessStepSuper
from mod.subprocess.samtools import RunSamtools


class RunSamtoolsIndex(RunSubprocessStepSuper):
    def __init__(self, input_bam, logger=None):
        custom_config = SamtoolsIndexCustomConfig()
        fixed_config = SamtoolsIndexFixedConfig()

        name = fixed_config.name
        output_dir = dirname(input_bam)
        execution_path = custom_config.execution_path

        version = custom_config.version
        version_flag = custom_config.version_flag
        version_parser = fixed_config.version_parser

        input_file = fixed_config.input_file
        output_file = fixed_config.output_file

        args = custom_config.args

        log_name = fixed_config.log_name
        logger = logger

        # Adjusting attributes based on relevant input variables
        input_file.arg = input_bam

        output_file.arg = input_bam

        super().__init__(name=name, output_dir=output_dir, execution_path=execution_path, version=version,
                         version_flag=version_flag, version_parser=version_parser, input_file=input_file,
                         output_file=output_file, args=args, log_name=log_name, logger=logger)

        self.samtools = RunSamtools(logger=self.logger)

    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parser=False):
        self.samtools.run()

    def save_log(self):
        pass

    def run(self, make_output_dir=True):
        super().run(make_output_dir=False)

    def format_command(self):
        command = [self.execution_path, self.input_file.arg]

        return SPACE.join(command)
