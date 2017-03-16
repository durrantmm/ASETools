import subprocess

from mod.misc.string_constants import *
from mod.pipeline.config.custom import SamtoolsIndexCustomConfig
from mod.pipeline.config.fixed import SamtoolsIndexFixedConfig
from mod.pipeline.run_process.steps.samtools import RunSamtools
from mod.run_process_step_super import RunProcessStepSuper


class RunSamtoolsIndex(RunProcessStepSuper):

    def __init__(self, input_bam, logger=None):

        custom_config = SamtoolsIndexCustomConfig()
        fixed_config = SamtoolsIndexFixedConfig()

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

        # Adjusting attributes based on relevant input variables
        input.arg = input_bam

        super().__init__(name=name, output_dir=output_dir, execution_path=execution_path, version=version,
                         version_flag=version_flag, version_parser=version_parser, input=input,
                         output=output, args=args, log_name=log_name, logger=logger)

        self.samtools = RunSamtools(logger=self.logger)


    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parser=False):
        self.samtools.run()

    def save_log(self):
        pass

    def run(self, make_output_dir=True):
        super().run(make_output_dir=False)


    def format_command(self):

        command = [self.execution_path, self.input.arg]

        return SPACE.join(command)

