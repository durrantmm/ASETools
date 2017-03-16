import subprocess
from os.path import basename, join

from mod.subprocess.config.custom import SamtoolsSortCustomConfig

from mod.config.fixed import SamtoolsSortFixedConfig
from mod.misc.string_constants import *
from mod.run_process_step_super import RunProcessStepSuper
from mod.subprocess.samtools import RunSamtools


class RunSamtoolsSort(RunProcessStepSuper):

    def __init__(self, output_dir, input_bam, output_bam=None, logger=None):

        custom_config = SamtoolsSortCustomConfig()
        fixed_config = SamtoolsSortFixedConfig()

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

        super().__init__(name=name, output_dir=output_dir, execution_path=execution_path, version=version,
                         version_flag=version_flag, version_parser=version_parser, input=input,
                         output=output, args=args, log_name=log_name, logger=logger)

        self.samtools = RunSamtools(logger=self.logger)


    def handle_output_bam(self, output_bam, input_bam):
        if output_bam:
            return basename(output_bam)
        else:
            return basename(input_bam).split('.')[0]+'.sorted.bam'

    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parser=False):
        self.samtools.run()

    def format_command(self):

        command = [self.execution_path]
        command.extend([self.output.flag, join(self.output_dir, self.output.arg)])
        command.append(self.input.arg)

        return SPACE.join(command)

