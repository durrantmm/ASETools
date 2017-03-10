#!/usr/bin/env python3
from collections import OrderedDict
import os

### Global attributes and methods accessible to all classes
REFERENCE_GENOME_PATH = "/srv/gsfs0/projects/bhatt/mdurrant/BUTYRATE_brayon/references/hg19/ucsc.hg19.fasta"


class UserRunSTAR:

    def __init__(self):
        # Path to the star aligner, absolute path is preferred over aliases
        self.PATH = "/home/mdurrant/miniconda3/bin/STAR"
        # The version of STAR aligner. Change at your own risk.
        # These are the options for the STAR alignment command
        # If the argument is optional, set its value to None to exclude.
        self.VERSION = "STAR_2.5.2b"
        self.VERSION_FLAG = '--version'

        self.ARGS = OrderedDict([

            ("--genomeDir", "/srv/gsfs0/projects/bhatt/mdurrant/BUTYRATE_brayon/references/starGenomeUCSChg19"),
            ("--readFilesCommand", "zcat"),
            ("--runThreadN", 2),
            ("--genomeLoad", "NoSharedMemory"),
            ("--outFilterMultimapNmax", 20),
            ("--alignSJDBoverhangMin", 1),
            ("--outFilterMultimapNmax", 999),
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

        ])


class UserRunAddReadGroups:

    def __init__(self):
        self.JAVA_PATH = "/srv/gs1/software/java/jre1.8.0_66/bin/java"
        self.JAVA_VERSION = "1.8.0_66"
        self.JAVA_VERSION_FLAG = "-version"

        self.PATH = "/srv/gs1/software/java/jre1.8.0_66/bin/java -jar " \
                    "/srv/gs1/software/picard-tools/2.8.0/picard.jar AddOrReplaceReadGroups"
        self.VERSION = "2.8.0-SNAPSHOT"
        self.VERSION_FLAG = "--help"


        self.ARGS = OrderedDict([

            ("SO", "coordinate"),
            ("RGID", "id"),
            ("RGLB", "library"),
            ("RGPL", "platform"),
            ("RGPU", "machine"),
            ("RGSM", "sample")

        ])


class UserRunMarkDuplicates:
    def __init__(self):
        self.JAVA_PATH = "/srv/gs1/software/java/jre1.8.0_66/bin/java"
        self.JAVA_VERSION = "1.8.0_66"
        self.JAVA_VERSION_FLAG = "-version"

        self.PATH = "/srv/gs1/software/java/jre1.8.0_66/bin/java -jar " \
                    "/srv/gs1/software/picard-tools/2.8.0/picard.jar MarkDuplicates"
        self.VERSION = "2.8.0-SNAPSHOT"
        self.VERSION_FLAG = "--help"


        self.ARGS = OrderedDict([

            ("CREATE_INDEX", "true"),
            ("VALIDATION_STRINGENCY", "SILENT"),
            ("M", "output.metrics")

        ])