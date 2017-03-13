import subprocess, os
from mod.misc.exceptions import VersionError, ExecutionNotRanNoOutput
import json
from mod.misc.record_classes import FlagArg_to_tuple
from mod.misc.log import *
from mod.misc.string_constants import *
from io import StringIO

class RunPythonStepSuper:

    def __init__(self, name, output_dir, input, output, log_name, logger=None):

        self.name = name
        self.output_dir = output_dir

        self.input = input
        self.output = self.handle_output(output_dir, output)

        self.log_name = log_name
        self.logger = logger

        self.ran = False


    def run(self):
        os.makedirs(self.output_dir, exist_ok=True)
        Log.info_chk(self.logger, msg_starting_run.format(NAME=self.name))
        self.process()
        self.save_log()
        self.ran = True


    def process(self):
        raise NotImplementedError


    def save_log(self):
        Log.info_chk(self.logger, msg_saving_run_info.format(PATH=self.log_name))
        log_json = self.get_log_json()
        json.dump(log_json, open(self.get_log_path(), 'w'), indent=4)


    def get_log_json(self):
        log_json = {

            'name': self.name,
            'output_dir': self.output_dir,
            'input': self.input,
            'output': self.output

        }

        return log_json


    def get_log_path(self):
        return os.path.join(self.output_dir, self.log_name)


    def retrieve_output_path(self, default_output=True):
        if default_output is True and isinstance(default_output, bool):
            output = self.output
        else:
            output = default_output

        if self.ran:
            return os.path.join(self.output_dir, os.path.basename(output))
        else:
            raise ExecutionNotRanNoOutput(self.name)

    def handle_output(self, output_dir, output):
        output_dir = os.path.abspath(os.path.realpath(output_dir))
        output = os.path.abspath(os.path.abspath(output))
        if output.startswith(output):
            return output
        else:
            return os.path.join(output_dir, os.path.basename(output))
