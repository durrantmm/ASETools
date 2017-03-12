import sys
from mod.misc.string_constants import *

class StarAlignCustomConfig:

    def __init__(self):

        self.execution_path = "/home/mdurrant/miniconda3/bin/STAR"
        self.version = "STAR_2.5.2b"
        self.version_flag = "--version"

        self.args = [

            ("--genomeDir", "/srv/gsfs0/projects/bhatt/mdurrant/BUTYRATE_brayon/references/starGenomeUCSChg19"),
            ("--readFilesCommand", "zcat"),
            ("--runThreadN", 2),
            ("--genomeLoad", "NoSharedMemory"),
            ("--outFilterMultimapNmax", 20),
            ("--alignSJoverhangMin", 8),
            ("--alignSJDBoverhangMin", 1),
            ("--outFilterMismatchNmax", 999),
            ("--outFilterMismatchNoverReadLmax", 0.04),
            ("--alignIntronMin", 20),
            ("--alignIntronMax", 1000000),
            ("--alignMatesGapMax", 1000000),
            ("--outSAMunmapped", "Within"),
            ("--outFilterType", "BySJout"),
            ("--outSAMattributes", "NH HI AS NM MD"),
            ("--sjdbScore", 1),
            ("--twopassMode", "Basic"),
            ("--twopass1readsN", -1)

        ]

class JavaCustomConfig:

    def __init__(self):

        self.execution_path = "/srv/gs1/software/java/jre1.8.0_66/bin/java"
        self.version = "1.8.0_66"
        self.version_flag = "-version"

        self.args = None


class PicardAddReadGroupsCustomConfig:

    def __init__(self):

        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-jar",
                                          "/srv/gs1/software/picard-tools/2.8.0/picard.jar",
                                          "AddOrReplaceReadGroups"])

        self.version = "2.8.0-SNAPSHOT"
        self.version_flag = "--help"

        self.args = [

            ("SO", "coordinate"),
            ("RGID", "id"),
            ("RGLB", "library"),
            ("RGPL", "platform"),
            ("RGPU", "machine"),
            ("RGSM", "sample")

        ]


class PicardMarkDuplicatesCustomConfig:
    from collections import OrderedDict

    def __init__(self):

        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-jar",
                                          "/srv/gs1/software/picard-tools/2.8.0/picard.jar",
                                          "MarkDuplicates"])

        self.version = "2.8.0-SNAPSHOT"
        self.version_flag = "--help"

        self.ARGS = [

            ("CREATE_INDEX", "true"),
            ("VALIDATION_STRINGENCY", "SILENT"),
            ("M", "output.metrics")

        ]