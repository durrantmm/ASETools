import sys
from mod.misc.record_classes import FlagTwoArgs, FlagArg
from mod.pipeline.version_parsers import parse_star_version

class StarAlignFixedConfig:

    def __init__(self):

        self.name = "STAR"

        self.input = FlagTwoArgs(flag='--readFilesIn', arg1=None, arg2=None)

        self.output = FlagArg(flag='--outFileNamePrefix', arg=None)

        self.version_parser = parse_star_version

        self.log_name = "star_align.json"