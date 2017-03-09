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


class CallVariantsRNAConfig:
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

        self.readFilesIn = ("--readFilesIn", None, None)

        self.outFileNamePrefix = ("--outFileNamePrefix", "STAR_algnmnt")

    def get_STAR_out_prefix_command(self, output_dir):
        return os.path.join(output_dir, self.outFileNamePrefix_ARG)


    def format_command_args(self, output_dir, delim=STR_CONST.SPACE):

        out_command = [self.PATH]
        for key, value in self.ARGS.items():
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