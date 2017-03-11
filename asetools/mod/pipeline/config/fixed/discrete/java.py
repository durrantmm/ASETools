from mod.pipeline.config.custom.discrete.java import CustomConfigJava
from mod.misc.record_classes import FlagArg, FlagTwoArgs

class FixedConfigJava(CustomConfigJava):

    def __init__(self):
        super().__init__()
        self.name = "Java"

        self.input = None

        self.output = None