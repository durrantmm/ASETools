"""
AUTHOR: Matt Durrant

This module contains a RunSubprocessStepSuper subclass called RunGATKPrintReads.

It executes the GATK PrintReads command using the subprocess standard library module.
"""

import subprocess
from os.path import basename, join
from mod.config.custom import GATKPrintReadsCustomConfig
from mod.config.fixed import GATKPrintReadsFixedConfig
from mod.misc.string_constants import *
from mod.subprocess_step_superclass import RunSubprocessStepSuper
from mod.subprocess.java import RunJava


class RunGATKPrintReads(RunSubprocessStepSuper):
    def __init__(self, output_dir, input_bam, input_recal_table, output_bam=None, logger=None):

        custom_config = GATKPrintReadsCustomConfig()
        fixed_config = GATKPrintReadsFixedConfig()

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
        input_file.arg = input_bam
        output_file.arg = self.handle_output_bam(output_bam, input_bam)

        # Adding a java step to check its version
        self.java = RunJava(logger=logger)
        self.input_recal_table = fixed_config.input_recal_table
        self.input_recal_table.arg = input_recal_table

        super().__init__(name=name, output_dir=output_dir, execution_path=execution_path, version=version,
                         version_flag=version_flag, version_parser=version_parser, input_file=input_file,
                         output_file=output_file, args=args, log_name=log_name, logger=logger)

    def handle_output_bam(self, output_bam, input_bam):
        if output_bam:
            return basename(output_bam)
        else:
            output_bam = basename(input_bam).split('.')[0] + '.RECAL.bam'
            return basename(output_bam)

    def format_command(self):

        command = [self.execution_path, SPACE.join([self.input_file.flag, self.input_file.arg]),
                   SPACE.join([self.input_recal_table.flag, self.input_recal_table.arg]),
                   SPACE.join([self.output_file.flag, join(self.output_dir, self.output_file.arg)])]
        command.extend([SPACE.join(map(str, [flag, arg])) for flag, arg in self.args])

        return SPACE.join(command)

    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parse=False):
        self.java.check_version()
        super().check_version()
