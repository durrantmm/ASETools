import sys, os, subprocess
from os.path import join
from mod.misc.string_constants import *
class QSubmit:

    def __init__(self, output_dir, qsub_script, command, qsub_flag='--qsub'):

        self.output_dir = output_dir
        self.qsub_execution_path = 'qsub'
        self.python_execution_path = 'python'
        self.output_file = 'job_submission.sh'
        self.qsub_script = qsub_script
        self.command = command
        self.qsub_flag = qsub_flag


    def submit(self):
        os.makedirs(self.output_dir, exist_ok=True)
        command = self.remove_qsub_flag(self.command, self.qsub_flag)
        self.create_submission_script(command)
        self.execute_qsub(command)


    def remove_qsub_flag(self, command, qsub_flag):
        command = command.split()
        qsub_index = command.index(qsub_flag)
        command = command[:qsub_index] + command[qsub_index+2:]
        return SPACE.join([self.python_execution_path]+command)

    def create_submission_script(self, command):
        with open(self.qsub_script) as infile:

            with open(join(self.output_dir, self.output_file), 'w') as outfile:

                for line in infile:
                    outfile.write(line)
                outfile.write(command)

    def execute_qsub(self, command):
        subprocess.check_call(['qsub', join(self.output_dir, self.output_file)])
