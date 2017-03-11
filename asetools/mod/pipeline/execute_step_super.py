import subprocess, os
from mod.misc.exceptions import VersionError
import json
from collections import OrderedDict
from mod.misc.record_classes import FlagArg_to_tuple
from mod.misc.log import *
from mod.misc.string_constants import *

class ExecutionStepSuper:

    def __init__(self):
        self.name = None
        self.output_dir = None
        self.execution_path = None


        self.version = None
        self.version_flag = None
        self.version_parser = None
        self.args = None

        self.input = None
        self.output = None
        self.log_name = 'asetools.log'

        self.logger = None


    def check_version(self, stderr=subprocess.PIPE, ignore_error=False):
        Log.info(self.logger, msg_checking_version.format(NAME=self.name, VERSION=self.name))
        try:

            output = subprocess.check_output(self.execution_path.split() + self.version_flag.split(), stderr=stderr)

        except subprocess.CalledProcessError as e:
            if ignore_error:
                output = e.output
            else:
                raise e

        local_version = self.version_parser(output)

        if self.version != local_version:
            raise VersionError(self.name, self.version, local_version)


    def run(self):
        Log.info(self.logger, msg_starting_run.format(NAME=self.name))
        os.makedirs(self.output_dir)
        self.check_version()
        self.execute_command()
        self.save_log()


    def execute_command(self, stderr=subprocess.PIPE):
        command = self.format_command()
        Log.info(self.logger, msg_executing_command.format(DELIM=NL, COMMAND=command))
        output = subprocess.check_output(command.split(), stderr=stderr)


    def save_log(self):
        Log.info(self.logger, msg_saving_run_info.format(self.log_name))
        log_json = self.get_log_json()
        json.dumps(log_json, self.get_log_path())


    def format_command(self):
        raise NotImplementedError


    def get_log_json(self, input_class_parse=FlagArg_to_tuple, output_class_parse=FlagArg_to_tuple):
        log_json = OrderedDict({

            ('name', self.name,),
            ('output_dir', self.output_dir),
            ('execution_path', self.execution_path),
            ('version', 'version'),
            ('input', input_class_parse(self.input)),
            ('output', output_class_parse(self.output))

        })

        return log_json


    def get_log_path(self):
        return os.path.join(self.output_dir, self.log_name)