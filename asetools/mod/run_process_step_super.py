import subprocess, os
from mod.misc.exceptions import VersionError, ExecutionNotRanNoOutput
import json
from mod.misc.record_classes import FlagArg_to_tuple
from mod.misc.log import *
from mod.misc.string_constants import *
from io import StringIO

class RunProcessStepSuper:

    def __init__(self, name, output_dir, execution_path, version, version_flag, version_parser, input, output, args,
                 log_name, logger=None):

        self.name = name
        self.output_dir = output_dir
        self.execution_path = execution_path


        self.version = version
        self.version_flag = version_flag
        self.version_parser = version_parser

        self.input = input
        self.output = output

        self.args = args

        self.log_name = log_name
        self.logger = logger

        self.ran = False


    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parser=False):
        Log.info_chk(self.logger, msg_checking_version.format(NAME=self.name, VERSION=self.version))
        Log.debug_chk(self.logger, msg_check_version_signature.format(STDERR=stderr, IGNORE_E=ignore_error,
                                                                      PVTP=pass_version_to_parser))
        try:
            Log.debug_chk(self.logger, SPACE.join(self.execution_path.split() + self.version_flag.split()))
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


    def run(self, make_output_dir=True):
        Log.info_chk(self.logger, msg_starting_run.format(NAME=self.name))

        if make_output_dir:
            os.makedirs(self.output_dir, exist_ok=True)

        self.check_version()
        self.execute_command()
        self.save_log()
        self.ran = True
        return self.retrieve_output_path()


    def execute_command(self, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False):
        command = self.format_command()
        Log.info_chk(self.logger, msg_executing_command.format(DELIM=NL, COMMAND=command))
        Log.debug_chk(self.logger, msg_execute_command_signature.format(STDERR=stderr, SHELL=shell))

        try:
            if not shell:
                command = command.split()

            popen = subprocess.Popen(command, stdout=stdout, stderr=stderr, shell=shell, universal_newlines=True)

            for stdout_line in iter(popen.stdout.readline, ""):
                Log.info_chk(self.logger, stdout_line.strip())
            popen.stdout.close()

            return_code = popen.wait()

            if return_code:
                raise subprocess.CalledProcessError(return_code, command)

        except subprocess.CalledProcessError as e:
            print(e.output)
            raise e



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
            return os.path.join(self.output_dir, os.path.basename(output))
        else:
            raise ExecutionNotRanNoOutput(self.name)