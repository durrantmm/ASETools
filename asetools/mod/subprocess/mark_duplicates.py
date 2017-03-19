"""
This module contains a RunSubprocessStepSuper subclass called RunPicardMarkDuplicates.

It executes the picard.jar MarkDuplicates command using the subprocess standard library module.
"""

import subprocess
from os.path import basename, join
from mod.config.custom import PicardMarkDuplicatesCustomConfig
from mod.config.fixed import PicardMarkDuplicatesFixedConfig
from mod.misc.string_constants import *
from mod.subprocess_step_superclass import RunSubprocessStepSuper
from mod.subprocess.java import RunJava


class RunPicardMarkDuplicates(RunSubprocessStepSuper):

    def __init__(self, output_dir, input_bam, output_bam = None, logger=None):

        custom_config = PicardMarkDuplicatesCustomConfig()
        fixed_config = PicardMarkDuplicatesFixedConfig()

        name = fixed_config.name
        output_dir = output_dir
        execution_path = custom_config.execution_path

        version = custom_config.version
        version_flag = custom_config.version_flag
        version_parser = fixed_config.version_parser

        input = fixed_config.input
        output = fixed_config.output

        args = custom_config.args

        log_name = fixed_config.log_name
        logger = logger

        # Adjusting attributes based on relevant input variables
        input.arg = input_bam
        output.arg = self.handle_output_bam(output_bam, input_bam)

        # Adding a java step to check its version
        self.java = RunJava(logger=logger)

        super().__init__(name=name, output_dir=output_dir, execution_path=execution_path, version=version,
                         version_flag=version_flag, version_parser=version_parser, input=input,
                         output=output, args=args, log_name=log_name, logger=logger)


    def handle_output_bam(self, output_bam, input_sam):
        if output_bam:
            return basename(output_bam)
        else:
            output_bam = basename(input_sam).split('.')[0] + '.bam'
            return basename(output_bam)


    def format_command(self):

        command = [self.execution_path, EQ.join([self.input.flag, self.input.arg])]
        for flag, arg in self.args:
            if flag == 'M':
                arg = join(self.output_dir, arg)
            command.append(EQ.join(map(str, [flag, arg])))
        command.append(EQ.join([self.output.flag, join(self.output_dir, self.output.arg)]))

        return SPACE.join(command)


    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parse=False):
        self.java.check_version()
        super().check_version(stderr=subprocess.STDOUT, ignore_error=True, pass_version_to_parser=True)
