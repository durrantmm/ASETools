"""
This module contains the QSubmit class, which is designed to take a python asetools command and an SGE submission
script and to resubmit the command to that it can be executed on the cluster.
"""

import os, subprocess
from os.path import join
from mod.misc.string_constants import *


class QSubmit:
    """
    Resubmits a command as an SGE job submission.
    """

    def __init__(self, output_dir, qsub_script, command, qsub_flag='--qsub'):
        """
        This is the constructor for QSubmit.
        :param output_dir: The output directory where all the downstream analysis will be saved.
        :param qsub_script: A path to a SGE submission script template.
        :param command: The command to be executed by the SGE submission script.
        :param qsub_flag: The qsub flag that needs to be stripped from the given command.
        """

        self.output_dir = output_dir
        self.qsub_execution_path = 'qsub'
        self.python_execution_path = 'python'
        self.output_file = 'job_submission.sh'
        self.qsub_script = qsub_script
        self.command = command
        self.qsub_flag = qsub_flag


    def submit(self):
        """
        Creates the output direct, reformats the command, and executes the qsub SGE submission
        :return:
        """
        os.makedirs(self.output_dir, exist_ok=True)
        command = self.remove_qsub_flag(self.command, self.qsub_flag)
        self.create_submission_script(command)
        self.execute_qsub()


    def remove_qsub_flag(self, command, qsub_flag):
        """
        Removes the qsub flag from the command to avoid an infinite loop.
        :param command: The command that needs to be fixed.
        :param qsub_flag: The qsub flag that needs to be stripped.
        :return: The reformatted command.
        """
        command = command.split()
        qsub_index = command.index(qsub_flag)
        command = command[:qsub_index] + command[qsub_index+2:]
        return SPACE.join([self.python_execution_path]+command)


    def create_submission_script(self, command):
        """
        Takes the submission script, makes a copy of it that contains the command to be executed at the bottom.
        :param command: The command to be added to the submission script.
        :return:
        """
        with open(self.qsub_script) as infile:

            with open(join(self.output_dir, self.output_file), 'w') as outfile:

                for line in infile:
                    outfile.write(line)
                outfile.write(command)


    def execute_qsub(self):
        """
        Uses subprocess module to execute the qsub command on the newly created script.
        :param command: The
        :return:
        """
        subprocess.check_call(['qsub', join(self.output_dir, self.output_file)])
