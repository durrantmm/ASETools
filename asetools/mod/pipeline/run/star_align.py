from os.path import basename
from mod.pipeline.config.fixed.discrete.star_align import ConfigStarAlign
from mod.misc.path_methods import get_shared_prefix
from mod.misc.string_constants import *
from mod.misc.record_classes import FlagTwoArgs_to_tuple
from mod.misc.log import SimpleLog

import os
import json
from glob import glob

class RunStarAlign(ConfigStarAlign):

    def __init__(self, output_dir, fastq1, fastq2, logger=None, out_prefix=None):
        super().__init__()

        self.logger = logger

        self.output_dir = output_dir

        self.input.arg1, self.input.arg2 = fastq1, fastq2

        self.output.arg = self.handle_out_prefix(out_prefix, fastq1, fastq2)

    def handle_out_prefix(self, out_prefix, fastq1, fastq2):
        if out_prefix:
            return out_prefix
        else:
            prefix = get_shared_prefix(fastq1, fastq2, strip_chars=[DOT, UND], base=True)
            return os.path.join(self.output_dir, prefix)

    def format_command(self):

        command = [self.execution_path]
        command.extend([self.input.flag, self.input.arg1, self.input.arg2])
        command.extend([SPACE.join(map(str, [flag, arg])) for flag, arg in self.args])
        command.extend([self.output.flag, self.output.arg])

        return SPACE.join(command)

    def get_log_json(self):
        return super().get_log_json(input_class_parse=FlagTwoArgs_to_tuple)

    def retrieve_output_path(self):
        print(self.output.arg+'*.sam')
        output = glob(os.path.join(self.output_dir, self.output.arg)+'*.sam')[0]
        return super().retrieve_output_path(default_output=output)

