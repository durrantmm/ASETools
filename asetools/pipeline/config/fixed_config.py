#!/usr/bin/env python3
from collections import OrderedDict
import os
from config.user_config import *

### Global attributes and methods accessible to all classes
STR_CONST = type("StringConstants", (),
                 {'UTF8':'utf-8',
                  'EMPTY_STRING': '',
                  'CONFIG_SUFFIX': '.config',
                  'SPACE': ' '})

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
            self.OUTPUT_DIR, self.STAR_ALIGN_READS+STR_CONST.CONFIG_SUFFIX)

        self.PICARD_ADD_OR_REPLACE_READ_GROUPS_CONFIG_PATH = os.path.join(
            self.OUTPUT_DIR, self.PICARD_ADD_OR_REPLACE_READ_GROUPS + STR_CONST.CONFIG_SUFFIX)

        self.PICARD_MARK_DUPLICATES_CONFIG_PATH = os.path.join(
            self.OUTPUT_DIR, self.PICARD_MARK_DUPLICATES+STR_CONST.CONFIG_SUFFIX)


class RunSTAR(UserRunSTAR):

    def __init__(self):
        super().__init__()

        self.PARSE_VERSION = lambda x: x.decode(STR_CONST.UTF8).strip()
        self.VERSION_ERROR = "The STAR aligner is version {ACTUAL}, not {EXPECTED}, as specified in the config file."

        self.readFilesIn_FLAG = "--readFilesIn"
        self.readFilesIn_ARG = None

        self.outFileNamePrefix_FLAG = "--outFileNamePrefix"
        self.outFileNamePrefix_ARG = "STAR_algnmnt"

        self.STAR_OPTIONAL_COMMAND_DICT = OrderedDict([(self.genomeDir_FLAG, self.genomeDir_ARG),
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
                                              (self.twopass1readsN_FLAG, self.twopass1readsN_ARG)])

    def get_STAR_out_prefix_command(self, output_dir):
        return os.path.join(output_dir, self.outFileNamePrefix_ARG)

    # Misc functions
    def format_command_args(self, output_dir, delim=STR_CONST.SPACE):

        out_command = [self.PATH]
        for key, value in self.STAR_OPTIONAL_COMMAND_DICT.items():
            if not value:
                continue
            if isinstance(value, list) or isinstance(value, set):
                out_command.append(delim.join(map(str, [key, delim.join(map(str, value))])))
            else:
                out_command.append(delim.join(map(str, [key, value])))

        out_command.append(self.outFileNamePrefix_FLAG)
        out_command.append(self.get_STAR_out_prefix_command(output_dir))

        return delim.join(out_command)

class Java(UserJava):
    def __init__(self):
        super().__init__()
        self.PARSE_VERSION = lambda x: x
        self.VERSION_ERROR = "Your java is version {ACTUAL}, not {EXPECTED}, as specified in the config file."


class RunPicard(UserRunPicard):
    def __init__(self):
        super().__init__()



class RunPicardAddOrReplaceReadGroups(UserRunPicardAddOrReplaceReadGroups):
    def __init__(self):
        super().__init__()

        self.INPUT_FLAG = "I="
        self.INPUT_ARG = None

        self.OUTPUT_FLAG = "O="
        self.OUTPUT_ARG = None


class RunPicardMarkDuplicates(UserRunPicardMarkDuplicates):
    def __init__(self):
        super().__init__()
