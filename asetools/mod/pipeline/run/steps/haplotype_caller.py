import os
import subprocess
from os.path import basename, join

from mod.misc.string_constants import *
from mod.pipeline.run.run_step_super import RunStepSuper
from mod.pipeline.config.custom import GATKRNAseqBaseRecalibratorCustomConfig
from mod.pipeline.config.fixed import GATKRNAseqBaseRecalibratorFixedConfig
from mod.pipeline.run.steps.java import RunJava

class RunGATKHaplotypeCaller(RunStepSuper):

    def __init__(self, output_dir, input_bam, output_vcf=None, logger=None):

        custom_config = GATKRNAseqBaseRecalibratorCustomConfig()
        fixed_config = GATKRNAseqBaseRecalibratorFixedConfig()

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
        output.arg = self.handle_output_vcf(output_vcf, input_bam)

        # Adding a java step to check its version
        self.java = RunJava(logger=logger)

        super().__init__(name=name, output_dir=output_dir, execution_path=execution_path, version=version,
                         version_flag=version_flag, version_parser=version_parser, input=input,
                         output=output, args=args, log_name=log_name, logger=logger)


    def handle_output_vcf(self, output_vcf, input_bam):
        if output_vcf:
            return basename(output_vcf)
        else:
            output_vcf = basename(input_bam).split('.')[0] + '.vcf'
            return basename(output_vcf)


    def format_command(self):

        command = [self.execution_path]
        command.append(SPACE.join([self.input.flag, self.input.arg]))
        command.extend([SPACE.join(map(str, [flag, arg])) for flag, arg in self.args])
        command.append(SPACE.join([self.output.flag, join(self.output_dir, self.output.arg)]))

        return SPACE.join(command)


    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parse=False):
        self.java.check_version()
        super().check_version()

