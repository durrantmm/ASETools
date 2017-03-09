#!/usr/bin/env python3
from collections import OrderedDict
import os

### Global attributes and methods accessible to all classes
STR_CONST = type("StringConstants", (),
                 {'UTF8':'utf-8',
                  'EMPTY_STRING': '',
                  'CONFIG_SUFFIX': '.config'})

REFERENCE_GENOME_PATH = "/srv/gsfs0/projects/bhatt/mdurrant/BUTYRATE_brayon/references/hg19/ucsc.hg19.fasta"


class Config:
    def __init__(self):
        self.PipelineFlow = PipelineFlow(self)
        self.RunSTAR = RunSTAR()

        # General reference genome in fasta format. For example, ucsc.hg19.fasta


class PipelineFlow:

    def __init__(self, config_in):
        self.Config = config_in
        self.CallVariantsRNASeq = PipelineCallVariantsRNASeq(self)

        # Output dir, usually specified as a command line argument.
        self.MAIN_OUTPUT_DIR = None

    def update_main_output_path(self, path):
        self.MAIN_OUTPUT_DIR = os.path.abspath(path)
        os.makedirs(self.MAIN_OUTPUT_DIR, exist_ok=True)

        self.CallVariantsRNASeq.update_paths_relative(path)


class PipelineCallVariantsRNASeq:
    global STR_CONST

    def __init__(self, pipeline_flow_in):
        self.PipelineFlow = pipeline_flow_in

        self.OUTPUT_DIR = "call_variants_rna"

        self.STAR_ALIGN_READS = "align_reads"
        self.PICARD_ADD_OR_REPLACE_READ_GROUPS = "add_read_groups"
        self.PICARD_MARK_DUPLICATES = "mark_duplicates"

        self.ORDER = [self.STAR_ALIGN_READS, self.PICARD_ADD_OR_REPLACE_READ_GROUPS, self.PICARD_MARK_DUPLICATES]
        self.START = self.STAR_ALIGN_READS


    def update_paths_relative(self, main_output_dir):

        self.OUTPUT_DIR = os.path.join(
            main_output_dir, self.OUTPUT_DIR)
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)

        self.STAR_ALIGN_READS_CONFIG_PATH = os.path.join(
            main_output_dir, self.STAR_ALIGN_READS+STR_CONST.CONFIG_SUFFIX)
        os.makedirs(self.STAR_ALIGN_READS_CONFIG_PATH, exist_ok=True)

        self.PICARD_ADD_OR_REPLACE_READ_GROUPS_CONFIG_PATH = os.path.join(
            main_output_dir, self.PICARD_ADD_OR_REPLACE_READ_GROUPS + STR_CONST.CONFIG_SUFFIX)
        os.makedirs(self.PICARD_ADD_OR_REPLACE_READ_GROUPS_CONFIG_PATH, exist_ok=True)

        self.PICARD_MARK_DUPLICATES_CONFIG_PATH = os.path.join(
            main_output_dir, self.PICARD_MARK_DUPLICATES+STR_CONST.CONFIG_SUFFIX)
        os.makedirs(self.PICARD_MARK_DUPLICATES_CONFIG_PATH, exist_ok=True)


class RunSTAR:

    def __init__(self):
        # Path to the star aligner, absolute path is preferred over aliases
        self.PATH = "/home/mdurrant/miniconda3/bin/STAR"
        # The version of STAR aligner. Change at your own risk.
        # These are the options for the STAR alignment command
        # If the argument is optional, set its value to None to exclude.
        self.VERSION = "STAR_2.5.2b"
        self.VERSION_FLAG = '--version'
        self.PARSE_VERSION = lambda x: x.decode(STR_CONST.UTF8)
        self.VERSION_ERROR = "The STAR aligner is version {ACTUAL}, not {EXPECTED}, as specified in the config file."

        self.genomeDir_FLAG = "--genomeDir"
        self.genomeDir_ARG = "/srv/gsfs0/projects/bhatt/mdurrant/BUTYRATE_brayon/references/starGenomeUCSChg19"

        self.readFilesIn_FLAG = "--readFilesIn"
        self.readFilesIn_ARG = None

        self.readFilesCommand_FLAG = "--readFilesCommand"
        self.readFilesCommand_ARG = "zcat"

        self.runThreadN_FLAG = "--runThreadN"
        self.runThreadN_ARG = 2

        self.genomeLoad_FLAG = "--genomeLoad"
        self.genomeLoad_ARG = "NoSharedMemory"

        self.outFilterMultimapNmax_FLAG = "--outFilterMultimapNmax"
        self.outFilterMultimapNmax_ARG = 20

        self.alignSJDBoverhangMin_FLAG = "--alignSJDBoverhangMin"
        self.alignSJDBoverhangMin_ARG = 1

        self.outFilterMismatchNmax_FLAG = "--outFilterMultimapNmax"
        self.outFilterMismatchNmax_ARG = 999

        self.outFilterMismatchNoverReadLmax_FLAG = "--outFilterMismatchNoverReadLmax"
        self.outFilterMismatchNoverReadLmax_ARG = 0.04

        self.alignIntronMin_FLAG = "--alignIntronMin"
        self.alignIntronMin_ARG = 20

        self.alignIntronMax_FLAG = "--alignIntronMax"
        self.alignIntronMax_ARG = 1000000

        self.alignMatesGapMax_FLAG = "--alignMatesGapMax"
        self.alignMatesGapMax_ARG = 1000000

        self.outSAMunmapped_FLAG = "--outSAMunmapped"
        self.outSAMunmapped_ARG = "Within"

        self.outFilterType_FLAG = "--outFilterType"
        self.outFilterType_ARG = "BySJout"

        self.outSAMattributes_FLAG = "--outSAMattributes"
        self.outSAMattributes_ARG = ['NH', 'HI', 'AS', 'NM', 'MD']

        self.sjdbScore_FLAG = "--sjdbScore"
        self.sjdbScore_ARG = 1

        self.twopassMode_FLAG = "--twopassMode"
        self.twopassMode_ARG = "Basic"

        self.twopass1readsN_FLAG = "--twopass1readsN"
        self.twopass1readsN_ARG = -1

        self.outFileNamePrefix_FLAG = "--outFileNamePrefix"
        self.outFileNamePrefix_ARG = None

        self.STAR_COMMAND_DICT = OrderedDict([(self.genomeDir_FLAG, self.genomeDir_ARG),
                                              (self.readFilesIn_FLAG, self.readFilesIn_ARG),
                                              (self.readFilesCommand_FLAG, self.readFilesCommand_ARG),
                                              (self.runThreadN_FLAG, self.runThreadN_ARG),
                                              (self.genomeLoad_FLAG, self.genomeLoad_ARG),
                                              (self.outFilterMultimapNmax_FLAG, self.outFilterMultimapNmax_ARG),
                                              (self.alignSJDBoverhangMin_FLAG, self.alignSJDBoverhangMin_ARG),
                                              (self.outFilterMismatchNmax_FLAG, self.outFilterMismatchNmax_ARG),
                                              (self.outFilterMismatchNoverReadLmax_FLAG,
                                               self.outFilterMismatchNoverReadLmax_ARG),
                                              (self.alignIntronMin_FLAG, self.alignIntronMin_ARG),
                                              (self.alignIntronMax_FLAG, self.alignIntronMax_ARG),
                                              (self.alignMatesGapMax_FLAG, self.alignMatesGapMax_ARG),
                                              (self.outSAMunmapped_FLAG, self.outSAMunmapped_ARG),
                                              (self.outFilterType_FLAG, self.outFilterType_ARG),
                                              (self.outSAMattributes_FLAG, self.outSAMattributes_ARG),
                                              (self.sjdbScore_FLAG, self.sjdbScore_ARG),
                                              (self.twopassMode_FLAG, self.twopassMode_ARG),
                                              (self.twopass1readsN_FLAG, self.twopass1readsN_ARG),
                                              (self.outFileNamePrefix_FLAG, self.outFileNamePrefix_ARG)])

    def set_out_prefix(self, override=False):
        if config.RunSTAR.outFileNamePrefix_ARG:
            config.RunSTAR.outFileNamePrefix_ARG = os.path.join(config.PipelineFlow.CallVariantsRNASeq.OUTPUT_DIR,
                                                                config.RunSTAR.outFileNamePrefix_ARG)
        else:
            config.RunSTAR.outFileNamePrefix_ARG = os.path.join(config.PipelineFlow.CallVariantsRNASeq.OUTPUT_DIR,
                                                                basename(config.PipelineFlow.OUTPUT_DIR))


class Java:
    PATH = "/srv/gs1/software/java/jre1.8.0_66/bin/java"
    VERSION = "1.8.0_66"
    VERSION_FLAG = "-version"
    PARSE_VERSION = lambda x: x
    VERSION_ERROR = "Your java is version {ACTUAL}, not {EXPECTED}, as specified in the config file."


class RunPicard:
    PATH = "/srv/gs1/software/picard-tools/2.8.0/picard.jar"


class RunPicardAddOrReplaceReadGroups:
    INPUT_FLAG = "I="
    INPUT_ARG = None

    OUTPUT_FLAG = "O="
    OUTPUT_ARG = None

    SORT_ORDER_FLAG = "SO="
    SORT_ORDER_ARG = "coordinate"

    RGID_FLAG = "RGID="
    RGID_ARG = "id"

    RGLB_FLAG = "RGLB="
    RGLB_ARG = "library"

    RGPL_FLAG = "RGPL="
    RGPL_ARG = "platform"

    RGPU_FLAG = "RGPU="
    RGPU_ARG = "machine"

    RGSM_FLAG = "RGSM="
    RGSM_ARG = "sample"


class RunPicardMarkDuplicates:
    pass
