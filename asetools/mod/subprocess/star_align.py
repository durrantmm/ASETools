"""
AUTHOR: Matt Durrant

This module contains a RunSubprocessStepSuper subclass called RunStarAlign.

It executes the STAR mapping application using the subprocess standard library module.
"""

from glob import glob
from os.path import basename, join
from mod.config.custom import StarAlignCustomConfig
from mod.config.fixed import StarAlignFixedConfig
from mod.misc.path_methods import get_shared_prefix
from mod.misc.record_classes import flagtwoargs_to_tuple
from mod.misc.string_constants import *
from mod.subprocess_step_superclass import RunSubprocessStepSuper


class RunStarAlign(RunSubprocessStepSuper):
    def __init__(self, output_dir, fastq1, fastq2, logger=None, out_prefix=None):

        custom_config = StarAlignCustomConfig()
        fixed_config = StarAlignFixedConfig()

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
        input_file.arg1, input_file.arg2 = fastq1, fastq2
        output_file.arg = self.handle_out_prefix(out_prefix, fastq1, fastq2)

        super().__init__(name=name, output_dir=output_dir, execution_path=execution_path, version=version,
                         version_flag=version_flag, version_parser=version_parser, input_file=input_file,
                         output_file=output_file, args=args, log_name=log_name, logger=logger)

    def handle_out_prefix(self, out_prefix, fastq1, fastq2):
        if out_prefix:
            return basename(out_prefix)
        else:
            prefix = get_shared_prefix(fastq1, fastq2, strip_chars=[DOT, UND], base=True)
            return basename(prefix)

    def format_command(self):

        command = [self.execution_path]
        command.extend([self.input_file.flag, self.input_file.arg1, self.input_file.arg2])
        command.extend([SPACE.join(map(str, [flag, arg])) for flag, arg in self.args])
        command.extend([self.output_file.flag, join(self.output_dir, self.output_file.arg)])

        return SPACE.join(command)

    def get_log_json(self):
        return super().get_log_json(input_class_parse=flagtwoargs_to_tuple)

    def retrieve_output_path(self):
        output = glob(join(self.output_dir, self.output_file.arg) + '*.sam')[0]
        return super().retrieve_output_path(default_output=output)
