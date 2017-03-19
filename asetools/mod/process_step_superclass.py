"""
This module contains the RunProcessStepSuper superclass.

This functions acts as the superclass for all of the subclasses that are found in the mod.process directory.

This superclass makes much of the analyses object-oriented, which greatly eases the creation of new processes.
"""

from mod.misc.exceptions import ExecutionNotRanNoOutput
import json
from mod.misc.log import *
from mod.misc.string_constants import *


class RunProcessStepSuper:
    """
    This is super class that executes python analyses that take an input file from the environment, processes the
    input file with python, and then outputs a new file to a specified output directory.
    """

    def __init__(self, name, output_dir, input_file, output, log_name, logger=None, output_suffix='tsv'):
        """
        Constructor for the superclass.
        :param name: The name of the class
        :param output_dir: The output directory to save all output files.
        :param input_file: The path to the primary input file to be processed.
        :param output: The name of the output path.
        :param log_name: The path to the output log which is saved in json format.
        :param logger: The logger object for outputting all of the relevant log information.
        :param output_suffix: The suffix of the output file to be written.
        """
        self.name = name
        self.output_dir = output_dir

        self.input = input_file
        self.output_suffix = output_suffix
        self.output = self.handle_output(output_dir, output, input_file)
        self.log_name = log_name
        self.logger = logger


        self.ran = False


    def run(self):
        """
        This is the primary function to be executed. It performs all of the functions of the class in the correct
        sequence.
        :return: Path to the output file that was created.
        """
        # Makes the output directory, it's ok if it exists.
        os.makedirs(self.output_dir, exist_ok=True)
        # Logs that it is beginning to process the data
        Log.info_chk(self.logger, msg_starting_run.format(NAME=self.name))
        # Runs the actual process() script.
        self.process()
        # Saves the log informatoin as a json file
        self.save_log()
        # Changes the ran status to ran = True
        self.ran = True
        # Returns the path to the output file.
        return self.retrieve_output_path()


    def process(self):
        """
        This is the process script, which is the primary script that needs to be executed by all of the classes
        that inherit from this superclass. The function of this method depends entirely on how the method is implemented
        by children classes.
        """
        raise NotImplementedError


    def save_log(self):
        """
        Saves a relevant log file in json format to the output directory
        """
        Log.info_chk(self.logger, msg_saving_run_info.format(PATH=self.log_name))
        log_json = self.get_log_json()
        json.dump(log_json, open(self.get_log_path(), 'w'), indent=4)


    def get_log_json(self):
        """
        Produces the general format of the json file to be output to the output directory.
        This function can be overridden by subclasses as they see fit.
        """
        log_json = {

            'name': self.name,
            'output_dir': self.output_dir,
            'input': self.input,
            'output': self.output

        }

        return log_json


    def get_log_path(self):
        """
        :return: The path to the output log json file.
        """
        return os.path.join(self.output_dir, self.log_name)


    def retrieve_output_path(self, default_output=True):
        """
        This function retrieves the output path.
        :param default_output:
        :return:
        """
        if default_output is True and isinstance(default_output, bool):
            output = self.output
        else:
            output = default_output

        if self.ran:
            return os.path.join(self.output_dir, os.path.basename(output))
        else:
            raise ExecutionNotRanNoOutput(self.name)


    def handle_output(self, output_dir, output, input_file):
        """
        This method handles the output path by ensuring that it only outputs to the output directory.
        :param output_dir: The output directory.
        :param output: The output path
        :param input_file: the input file
        :return:
        """

        # If output does not exist or is in an incorrect path, it creates a proper output file.
        if not output or os.path.realpath(output) == os.path.realpath(input_file):
            output = os.path.basename(input_file).split(DOT)[0]+DOT+self.name+DOT+self.output_suffix

        return os.path.basename(output)
