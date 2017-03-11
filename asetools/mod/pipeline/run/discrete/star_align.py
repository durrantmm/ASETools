import os
from glob import glob

from mod.misc.path_methods import get_shared_prefix
from mod.misc.record_classes import FlagTwoArgs_to_tuple
from mod.misc.string_constants import *
from mod.pipeline.config.fixed.discrete.star_align import FixedConfigStarAlign
from run.discrete.version_parsers import parse_star_version
from os.path import basename


class RunStarAlign(FixedConfigStarAlign):

    def __init__(self, output_dir, fastq1, fastq2, logger=None, out_prefix=None):
        super().__init__()

        self.logger = logger

        self.output_dir = os.path.abspath(output_dir)

        self.input.arg1, self.input.arg2 = fastq1, fastq2

        self.output.arg = self.handle_out_prefix(out_prefix, fastq1, fastq2)

        self.version_parser = parse_star_version

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
        command.extend([self.output.flag, os.path.join(self.output_dir, self.output.arg)])

        return SPACE.join(command)

    def get_log_json(self):
        return super().get_log_json(input_class_parse=FlagTwoArgs_to_tuple)

    def retrieve_output_path(self):
        output = glob(self.output.arg+'*.sam')[0]
        return super().retrieve_output_path(default_output=output)

