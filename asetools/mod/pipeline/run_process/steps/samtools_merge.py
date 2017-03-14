from glob import glob
from os.path import basename, join
import os
import subprocess

from mod.misc.log import *
from mod.misc.record_classes import *
from mod.misc.record_classes import FlagArg
from mod.misc.string_constants import *
from mod.pipeline.config.custom import SamtoolsMergeCustomConfig
from mod.pipeline.config.fixed import SamtoolsMergeFixedConfig
from mod.pipeline.run_process.run_process_step_super import RunProcessStepSuper
from mod.pipeline.run_process.steps.samtools import RunSamtools


class RunSamtoolsMerge(RunProcessStepSuper):

    def __init__(self, output_dir, input_bam1, input_bam2, output_bam=None, logger=None):

        custom_config = SamtoolsMergeCustomConfig()
        fixed_config = SamtoolsMergeFixedConfig()

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
        input.arg1 = input_bam1
        input.arg2 = input_bam2
        output.arg = self.handle_output_bam(output_bam, input_bam1)

        super().__init__(name=name, output_dir=output_dir, execution_path=execution_path, version=version,
                         version_flag=version_flag, version_parser=version_parser, input=input,
                         output=output, args=args, log_name=log_name, logger=logger)

        self.samtools = RunSamtools(logger=self.logger)


    def handle_output_bam(self, output_bam, input_bam):
        if output_bam:
            return basename(output_bam)
        else:
            return basename(input_bam).split('.')[0]+'merged.bam'

    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parser=False):
        self.samtools.run()

    def format_command(self):

        command = [self.execution_path]
        command.append(self.input.arg1)
        command.append(self.input.arg2)
        command.append(join(self.output_dir, self.output.arg))

        return SPACE.join(command)

