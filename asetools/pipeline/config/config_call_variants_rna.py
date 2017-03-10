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
        self.INVALID_FASTQ = "At least one of the fastq files you provided is invalid."
        self.ABSENT_FASTQ = "If you are running the call variants pipeline from the read alignment step, you must " \
                            "provide valid fastq files with the --readFilesIn command"

        self.readFilesIn = type("readFilesIn", (), {"flag": "--readFilesIn",
                                                    'fastq1': None,
                                                    'fastq2': None})

        self.outFileNamePrefix = type('outFileNamePrefix', (), {'flag': "--outFileNamePrefix",
                                                                'prefix': None})

    def get_STAR_out_prefix_command(self, output_dir):
        return os.path.join(output_dir, self.outFileNamePrefix.prefix)


    def format_command_args(self, output_dir, delim=STR_CONST.SPACE):

        assert self.readFilesIn.fastq1 and self.readFilesIn.fastq2, self.ABSENT_FASTQ

        out_command = [self.PATH, self.readFilesIn.flag, self.readFilesIn.fastq1, self.readFilesIn.fastq2]
        for key, value in self.ARGS.items():
            if not value:
                continue
            if isinstance(value, list) or isinstance(value, set):
                out_command.append(delim.join(map(str, [key, delim.join(map(str, value))])))
            else:
                out_command.append(delim.join(map(str, [key, value])))

        out_command.append(delim.join(self.outFileNamePrefix))
        out_command.append(self.get_STAR_out_prefix_command(output_dir))

        return delim.join(out_command)


    def set_readFilesIn(self, read_files_in, make_prefix=False):
        assert len(read_files_in) == 2, self.INVALID_FASTQ
        assert os.path.isfile(read_files_in[0]), self.INVALID_FASTQ
        assert os.path.isfile(read_files_in[1]), self.INVALID_FASTQ
        self.readFilesIn.fastq1, self.readFilesIn.fastq2 = read_files_in

        if make_prefix:
            prefix = ""
            i = 0
            l1, l2 = self.readFilesIn.fastq1[i], self.readFilesIn.fastq2[i]
            while l1 == l2:
                i += 1
                prefix += l1
                l1, l2 = self.readFilesIn.fastq1[i], self.readFilesIn.fastq2[i]
            self.outFileNamePrefix.prefix = prefix.strip('.').strip('_')



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
