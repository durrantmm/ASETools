from os.path import basename
from mod.pipeline.config.fixed.discrete.star_align import ConfigStarAlign
from mod.misc.string_methods import get_shared_prefix
from mod.misc.string_constants import SPACE
from mod.misc.record_classes import FlagTwoArgs

import json

class RunStarAlign(ConfigStarAlign):

    def __init__(self, output_dir, fastq1, fastq2, out_prefix=None):
        super().__init__()

        self.output_dir = output_dir

        self.input.arg1, self.input.arg2 = fastq1, fastq2

        self.output.arg = self.handle_out_prefix(out_prefix, fastq1, fastq2)

    def handle_out_prefix(self, out_prefix, fastq1, fastq2):
        if out_prefix:
            return out_prefix
        else:
            return get_shared_prefix(fastq1, fastq2)

    def format_command(self):

        command = [self.execution_path]
        command.extend([self.input.flag, self.input.arg1, self.input.arg2])
        command.extend([SPACE.join([flag, arg]) for flag, arg in self.args])
        command.extend([self.output.flag, self.output.arg])

        return SPACE.join(command)

    def save_log(self):
        log_json = self.get_log_json(input_class_parse=FlagTwoArgs)
        json.dumps(log_json, self.get_log_path())


