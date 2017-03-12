import sys
from mod.misc.string_constants import *


PICARD_EXECUTION_PATH = "/srv/gs1/software/picard-tools/2.8.0/picard.jar"
PICARD_VERSION = "2.8.0-SNAPSHOT"

REFERENCE_GENOME_FASTA = "/srv/gsfs0/projects/bhatt/mdurrant/BUTYRATE_brayon/references/hg19/ucsc.hg19.fasta"

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
                                          PICARD_EXECUTION_PATH,
                                          "AddOrReplaceReadGroups"])

        self.version = PICARD_VERSION
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

    def __init__(self):

        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-jar",
                                          PICARD_EXECUTION_PATH,
                                          "MarkDuplicates"])

        self.version = PICARD_VERSION
        self.version_flag = "--help"

        self.args = [

            ("CREATE_INDEX", "true"),
            ("VALIDATION_STRINGENCY", "SILENT"),
            ("M", "output.metrics")

        ]

class GATKSplitNCigarReadsCustomConfig:

    def __init__(self):
        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-jar",
                                          "/srv/gs1/software/gatk/gatk-3.6/GenomeAnalysisTK.jar",
                                          "-T SplitNCigarReads"])

        self.version = "3.6-0-g89b7209"
        self.version_flag = "--version"

        self.args = [

            ("-R", REFERENCE_GENOME_FASTA),
            ("-rf", "ReassignOneMappingQuality"),
            ("-RMQF", 255),
            ("-RMQT", 60),
            ("-U", "ALLOW_N_CIGAR_READS")

        ]
