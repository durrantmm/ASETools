"""
This module contains a RunSubprocessStepSuper subclass called RunSamtoolsMerge.

It executes the samtools merge command using the subprocess standard library module.
"""

import subprocess
from os.path import basename, join
from mod.config.custom import SamtoolsMergeCustomConfig
from mod.config.fixed import SamtoolsMergeFixedConfig
from mod.misc.record_classes import *
from mod.misc.string_constants import *
from mod.subprocess_step_superclass import RunSubprocessStepSuper
from mod.subprocess.samtools import RunSamtools


class RunSamtoolsMerge(RunSubprocessStepSuper):
    def __init__(self, output_dir, input_bam1, input_bam2, output_bam=None, logger=None):

        custom_config = SamtoolsMergeCustomConfig()
        fixed_config = SamtoolsMergeFixedConfig()

        name = fixed_config.name
        output_dir = output_dir
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
        input_file.arg1 = input_bam1
        input_file.arg2 = input_bam2
        output_file.arg = self.handle_output_bam(output_bam, input_bam1)

        super().__init__(name=name, output_dir=output_dir, execution_path=execution_path, version=version,
                         version_flag=version_flag, version_parser=version_parser, input_file=input_file,
                         output_file=output_file, args=args, log_name=log_name, logger=logger)

        self.samtools = RunSamtools(logger=self.logger)

    def handle_output_bam(self, output_bam, input_bam):
        if output_bam:
            return basename(output_bam)
        else:
            return basename(input_bam).split('.')[0] + '.merged.bam'

    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parser=False):
        self.samtools.run()

    def get_log_json(self, input_class_parse=flagarg_to_tuple, output_class_parse=flagarg_to_tuple):
        super().get_log_json(input_class_parse=flagtwoargs_to_tuple)

    def format_command(self):

        command = [self.execution_path]
        command.extend([SPACE.join(map(str, [flag, arg])) for flag, arg in self.args])
        command.append(join(self.output_dir, self.output_file.arg))
        command.append(self.input_file.arg1)
        command.append(self.input_file.arg2)

        return SPACE.join(command)
