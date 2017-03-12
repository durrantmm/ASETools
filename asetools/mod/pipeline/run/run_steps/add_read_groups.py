import os
import subprocess
from os.path import basename, join

from mod.misc.string_constants import *
from mod.pipeline.run.run_step_super import RunStepSuper
from mod.pipeline.config.custom import PicardAddReadGroupsCustomConfig
from mod.pipeline.config.fixed import PicardAddReadGroupsFixedConfig

class RunPicardAddReadGroups(RunStepSuper):

    def __init__(self, output_dir, input_sam, output_bam = None, logger=None, out_prefix=None):

        custom_config = PicardAddReadGroupsCustomConfig()
        fixed_config = PicardAddReadGroupsFixedConfig()

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
        input.arg = input_sam
        output.arg = self.handle_output_bam(out_prefix, input_sam)

        super().__init__(name, output_dir, execution_path, version, version_flag,
                         version_parser, input, output, args, log_name, logger)


    def handle_output_bam(self, output_bam, input_sam):
        if output_bam:
            return basename(output_bam)
        else:
            output_bam = basename(input_sam).split('.')[0] + '.bam'
            return basename(output_bam)


    def format_command(self):
        command = [self.execution_path]
        command.extend(EQ.join([self.input.flag, self.input.arg]))
        command.extend([EQ.join(map(str, [flag, arg])) for flag, arg in self.args])
        command.extend(EQ.join([self.output.flag, join(self.output_dir, self.output.arg)]))

        return SPACE.join(command)


    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parse=False):
        self.java.check_version()
        super().check_version(stderr=subprocess.STDOUT, ignore_error=False)

