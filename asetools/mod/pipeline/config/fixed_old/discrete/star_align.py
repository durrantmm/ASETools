from mod.misc.record_classes import FlagArg, FlagTwoArgs
from pipeline.config.discrete.star_align import CustomConfigStarAlign


class FixedConfigStarAlign(CustomConfigStarAlign):

    def __init__(self):
        super().__init__()
        self.name = "STAR"

        self.input = FlagTwoArgs(flag='--readFilesIn', arg1=None, arg2=None)

        self.output = FlagArg(flag='--outFileNamePrefix', arg=None)

        # JSON File Name
        self.log_name = "star_align.json"