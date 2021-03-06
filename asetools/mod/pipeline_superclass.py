"""
AUTHOR: Matt Durrant

This module contains the RunPipelineSuper supeclass.

This functions acts as the superclass for all of the pipelines that are found in the mod.pipelines directory.

This superclass makes much of the analyses object-oriented, which greatly eases the creation of new subclasses.
"""

from mod.misc.log import *


class RunPipelineSuper:
    """
    This class acts as a superclass for all pipelines in this package.
    """

    def __init__(self, name, output_dir, input_file, logger):

        self.name = name
        self.output_dir = output_dir

        self.input_file = input_file

        self.logger = logger

        self.ran = False


    def run(self):
        """
        Runs the pipeline in its entirety.
        :return:
        """
        Log.info_chk(self.logger, msg_starting_run.format(NAME=self.name))
        os.makedirs(self.output_dir, exist_ok=True)
        self.execute_steps()
        self.ran = True


    def execute_steps(self):
        """
        This needs to be implemented by the subclasses.
        This is the sequential execution of all pipeline steps.
        """
        raise NotImplementedError