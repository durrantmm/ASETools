import subprocess, os
from mod.misc.exceptions import VersionError, ExecutionNotRanNoOutput
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

        self.ran = False


    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parser=False):
        Log.info_chk(self.logger, msg_checking_version.format(NAME=self.name, VERSION=self.name))
        Log.debug_chk(self.logger, msg_check_version_signature.format(STDERR=stderr, IGNORE_E=ignore_error,
                                                                      PVTP=pass_version_to_parser))
        try:

            output = subprocess.check_output(self.execution_path.split() + self.version_flag.split(), stderr=stderr)

        except subprocess.CalledProcessError as e:
            if ignore_error:
                output = e.output
            else:
                raise e

        Log.debug_chk(self.logger, output)
        if pass_version_to_parser:
            local_version = self.version_parser(output, self.version)
        else:
            local_version = self.version_parser(output)

        if self.version != local_version:
            raise VersionError(self.name, self.version, local_version)


    def run(self):
        Log.info_chk(self.logger, msg_starting_run.format(NAME=self.name))
        os.makedirs(self.output_dir, exist_ok=True)
        self.check_version()
        self.execute_command()
        self.save_log()
        self.ran = True


    def execute_command(self, stderr=subprocess.PIPE):
        command = self.format_command()
        Log.info_chk(self.logger, msg_executing_command.format(DELIM=NL, COMMAND=command))
        #output = subprocess.check_output(command.split(), stderr=stderr)


    def save_log(self):
        Log.info_chk(self.logger, msg_saving_run_info.format(PATH=self.log_name))
        log_json = self.get_log_json()
        json.dump(log_json, open(self.get_log_path(), 'w'), indent=4)


    def get_log_json(self, input_class_parse=FlagArg_to_tuple, output_class_parse=FlagArg_to_tuple):
        log_json = {

            'name': self.name,
            'output_dir': self.output_dir,
            'execution_path': self.execution_path,
            'version': 'version',
            'input': input_class_parse(self.input),
            'output': output_class_parse(self.output),
            'custom_args': self.args

        }

        return log_json


    def get_log_path(self):
        return os.path.join(self.output_dir, self.log_name)


    def format_command(self):
        raise NotImplementedError


    def retrieve_output_path(self, default_output=True):
        if default_output is True and isinstance(default_output, bool):
            output = self.output.arg
        else:
            output = default_output

        if self.ran:
            return output
        else:
            raise ExecutionNotRanNoOutput(self.name)
