from mod.pipeline.config.custom.discrete.star_align import CustomConfigStarAlign
from mod.misc.string_constants import *
from mod.misc.record_classes import FlagArg, FlagTwoArgs
from mod.pipeline.run.version_parsers import parse_star_version

class ConfigStarAlign(CustomConfigStarAlign):

    def __init__(self):
        super().__init__()
        self.name = "STAR"

        self.input = FlagTwoArgs(flag='--readFilesIn', arg1=None, arg2=None)

        self.output = FlagArg(flag='--outFileNamePrefix', arg=None)

        # JSON File Name
        self.log_name = "star_align.json"

        # Version Parser lambda function
        self.version_parser = parse_star_version