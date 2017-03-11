import os
import subprocess

from mod.misc.string_constants import *
from mod.pipeline.config.fixed.discrete.add_read_groups import FixedConfigAddReadGroups
from run.discrete.version_parsers import parse_add_read_groups_version
from os.path import basename, join


class RunAddReadGroups(FixedConfigAddReadGroups):

    def __init__(self, output_dir, input_sam, output_bam=None, logger=None, out_prefix=None):
        super().__init__()

        self.logger = logger

        self.output_dir = os.path.abspath(output_dir)

        self.input.arg = input_sam

        self.output.arg = self.handle_output_bam(output_bam, input_sam)

        self.version_parser = parse_add_read_groups_version

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
        super().check_version(stderr=subprocess.STDOUT)

