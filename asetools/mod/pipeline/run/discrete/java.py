import os
from glob import glob

from mod.pipeline.config.fixed.discrete.java import FixedConfigJava
from run.discrete.version_parsers import parse_java_version
import subprocess


class RunJava(FixedConfigJava):

    def __init__(self, output_dir, fastq1, fastq2, logger=None, out_prefix=None):
        super().__init__()

        self.logger = logger

        self.version_parser = parse_java_version


    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parse=False):
        super().check_version(stderr=subprocess.STDOUT)

    def run(self):
        self.check_version()

    def execute_command(self):
        raise NotImplementedError

    def save_log(self):
        raise NotImplementedError

    def get_log_json(self):
        raise NotImplementedError

    def get_log_path(self):
        raise NotImplementedError

    def format_command(self):
        raise NotImplementedError


    def retrieve_output_path(self, default_output=True):
        raise NotImplementedError

