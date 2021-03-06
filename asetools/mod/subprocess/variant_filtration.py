"""
AUTHOR: Matt Durrant

This module contains a RunSubprocessStepSuper subclass called RunGATKVariantFiltration.

It executes the GATK VariantFiltration command using the subprocess standard library module.
"""

import subprocess
from os.path import basename, join
from mod.config.custom import GATKVariantFiltrationCustomConfig
from mod.config.fixed import GATKVariantFiltrationFixedConfig
from mod.misc.string_constants import *
from mod.subprocess_step_superclass import RunSubprocessStepSuper
from mod.subprocess.java import RunJava


class RunGATKVariantFiltration(RunSubprocessStepSuper):
    def __init__(self, output_dir, input_vcf, output_vcf=None, logger=None):

        custom_config = GATKVariantFiltrationCustomConfig()
        fixed_config = GATKVariantFiltrationFixedConfig()

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
        input_file.arg = input_vcf
        output_file.arg = self.handle_output_vcf(output_vcf, input_vcf)

        # Adding a java step to check its version
        self.java = RunJava(logger=logger)

        super().__init__(name=name, output_dir=output_dir, execution_path=execution_path, version=version,
                         version_flag=version_flag, version_parser=version_parser, input_file=input_file,
                         output_file=output_file, args=args, log_name=log_name, logger=logger)

    def handle_output_vcf(self, output_vcf, input_vcf):
        if output_vcf:
            return basename(output_vcf)
        else:
            output_bam = basename(input_vcf).split('.')[0] + '.FILTERED.vcf'
            return basename(output_bam)

    def format_command(self):

        command = [self.execution_path, SPACE.join([self.input_file.flag, self.input_file.arg]),
                   SPACE.join([self.output_file.flag, join(self.output_dir, self.output_file.arg)])]
        command.extend([SPACE.join(map(str, [flag, arg])) for flag, arg in self.args])

        return SPACE.join(command)

    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parse=False):
        self.java.check_version()
        super().check_version()

    def execute_command(self, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False):
        super().execute_command(shell=True)
