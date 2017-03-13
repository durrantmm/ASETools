from mod.misc.log import *


class RunPipedSuper:

    def __init__(self, name, output_dir, input, logger):

        self.name = name
        self.output_dir = output_dir

        self.input = input

        self.logger = logger

        self.ran = False


    def run(self):
        Log.info_chk(self.logger, msg_starting_run.format(NAME=self.name))
        os.makedirs(self.output_dir, exist_ok=True)
        self.execute_steps()
        self.ran = True


    def execute_steps(self):
        raise NotImplementedError