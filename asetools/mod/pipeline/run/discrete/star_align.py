import os
from glob import glob
from os.path import basename, join

from mod.misc.path_methods import get_shared_prefix
from mod.misc.record_classes import FlagTwoArgs_to_tuple
from mod.misc.string_constants import *
from mod.pipeline.config.custom import StarAlignCustomConfig
from mod.pipeline.config.fixed import StarAlignFixedConfig
from mod.pipeline.run_step_super import RunStepSuper


class RunStarAlign(RunStepSuper):

    def __init__(self, output_dir_in, fastq1_in, fastq2_in, logger_in=None, out_prefix_in=None):

        custom_config = StarAlignCustomConfig()
        fixed_config = StarAlignFixedConfig()

        name = fixed_config.name
        output_dir = output_dir_in
        execution_path = custom_config.execution_path

        version = custom_config.version
        version_flag = custom_config.version_flag
        version_parser = fixed_config.version_parser

        input = fixed_config.input
        output = fixed_config.output

        args = custom_config.args

        log_name = fixed_config.log_name
        logger = logger_in

        # Adjusting attributes based on relevant input variables
        input.arg1, input.arg2 = fastq1_in, fastq2_in
        output.arg = self.handle_out_prefix(out_prefix_in, fastq1_in, fastq2_in)

        super().__init__(name, output_dir, execution_path, version, version_flag,
                         version_parser, input, output, args, log_name, logger)


    def handle_out_prefix(self, out_prefix, fastq1, fastq2):
        if out_prefix:
            return basename(out_prefix)
        else:
            prefix = get_shared_prefix(fastq1, fastq2, strip_chars=[DOT, UND], base=True)
            return basename(prefix)


    def format_command(self):

        command = [self.execution_path]
        command.extend([self.input.flag, self.input.arg1, self.input.arg2])
        command.extend([SPACE.join(map(str, [flag, arg])) for flag, arg in self.args])
        command.extend([self.output.flag, join(self.output_dir, self.output.arg)])

        return SPACE.join(command)

    def get_log_json(self):
        return super().get_log_json(input_class_parse=FlagTwoArgs_to_tuple)

    def retrieve_output_path(self):
        output = glob(join(self.output_dir, self.output.arg)+'*.sam')[0]
        return super().retrieve_output_path(default_output=output)

