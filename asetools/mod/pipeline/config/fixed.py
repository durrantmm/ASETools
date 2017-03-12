import sys
from mod.misc.record_classes import FlagTwoArgs, FlagArg
from mod.pipeline.version_parsers import *

class StarAlignFixedConfig:

    def __init__(self):

        self.name = "STAR"

        self.input = FlagTwoArgs(flag='--readFilesIn', arg1=None, arg2=None)

        self.output = FlagArg(flag='--outFileNamePrefix', arg=None)

        self.version_parser = parse_star_version

        self.log_name = "star_align.json"


class JavaFixedConfig:

    def __init__(self):

        self.name = "Java"

        self.input = None

        self.output = None

        self.version_parser = parse_java_version

        self.log_name = None


class PicardAddReadGroupsFixedConfig:

    def __init__(self):
        self.name = "AddOrReplaceReadGroups"

        self.input = FlagArg(flag='I', arg=None)

        self.output = FlagArg(flag='O', arg=None)

        self.version_parser = parse_add_read_groups_version

        self.log_name = "add_read_groups.json"


class PicardMarkDuplicatesFixedConfig:

    def __init__(self):

        self.name = "MarkDuplicates"

        self.input = FlagArg(flag='I', arg=None)

        self.output = FlagArg(flag='O', arg=None)

        self.version_parser = parse_mark_duplicates_version

        self.log_name = "mark_duplicates.json"

class GATKSplitNCigarReadsFixedConfig:

    def __init__(self):

        self.name = "GATK-SplitNCigarReads"

        self.input = FlagArg(flag='-I', arg=None)

        self.output = FlagArg(flag='-o', arg=None)

        self.version_parser = parse_mark_duplicates_version

        self.log_name = "split_n_cigar_reads.json"