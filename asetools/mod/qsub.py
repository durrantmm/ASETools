import sys, os
from mod.misc.string_constants import *
class QSubmit:

    def __init__(self, output_dir, qsub_script, command, qsub_flag='--qsub'):

        self.output_dir = output_dir
        self.execution_path = 'python'
        self.qsub_script = qsub_script
        self.command = command
        self.qsub_flag = qsub_flag


    def submit(self):
        os.makedirs(self.output_dir)
        command = self.remove_qsub_flag(self.command, self.qsub_flag)
        self.create_submission_script(command)


    def remove_qsub_flag(self, command, qsub_flag):
        command = command.split()
        qsub_index = command.index(qsub_flag)
        command = command[:qsub_index] + command[qsub_index+2:]
        return SPACE.join(command)

    def create_submission_script(self, command):
        with open(self.qsub_script) as infile:
            for line in infile:
                print(line)