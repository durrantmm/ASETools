#!/usr/bin/env python3
from collections import OrderedDict
import os, sys
from os.path import basename
import json
from json import JSONEncoder
from config.user_config import *

### Global attributes and methods accessible to all classes
STR_CONST = type("StringConstants", (),
                 {'UTF8':'utf-8',
                  'EMPTY_STRING': '',
                  'SPACE': ' '})


class CallVariantsRNAConfig:
    def __init__(self):
        self.MAIN_OUTPUT_DIR = None

        self.RunSTAR = RunSTAR()

        self.STAR_ALIGN_READS = "align_reads"
        self.PICARD_ADD_OR_REPLACE_READ_GROUPS = "add_read_groups"
        self.PICARD_MARK_DUPLICATES = "mark_duplicates"

        self.ORDER = [self.STAR_ALIGN_READS, self.PICARD_ADD_OR_REPLACE_READ_GROUPS, self.PICARD_MARK_DUPLICATES]
        self.START = self.STAR_ALIGN_READS


    def update_main_output_path(self, path):
        self.MAIN_OUTPUT_DIR = os.path.abspath(path)
        os.makedirs(self.MAIN_OUTPUT_DIR, exist_ok=True)

        self.RunSTAR.update_paths_relative(self.MAIN_OUTPUT_DIR)


class RunSTAR(UserRunSTAR):

    def __init__(self):
        super().__init__()
        self.OUTPUT_DIR = "STEP1_STAR_alignment"

        self.STAR_ALIGN_READS_CONFIG_PATH = "star_alignment.config"

        self.PARSE_VERSION = lambda x: x.decode(STR_CONST.UTF8).strip()
        self.VERSION_ERROR = "The STAR aligner is version {ACTUAL}, not {EXPECTED}, as specified in the config file."
        self.INVALID_FASTQ = "At least one of the fastq files you provided is invalid."
        self.ABSENT_FASTQ = "If you are running the call variants pipeline from the read alignment step, you must " \
                            "provide valid fastq files with the --readFilesIn command"

        self.readFilesIn_FLAG = "--readFilesIn"
        self.readFilesIn_ARG1 = None
        self.readFilesIn_ARG2 = None
        self.readFilesIn = [self.readFilesIn_FLAG, self.readFilesIn_ARG1, self.readFilesIn_ARG2]


        self.outFileNamePrefix_FLAG = "--outFileNamePrefix"
        self.outFileNamePrefix_ARG = 'STAR_alnmn'
        self.outFileNamePrefix = [self.outFileNamePrefix_FLAG, self.outFileNamePrefix_ARG]

    def get_full_out_prefix(self):
        return os.path.join(self.OUTPUT_DIR, self.outFileNamePrefix_ARG)


    def format_command_args(self, delim=STR_CONST.SPACE):

        assert self.readFilesIn.fastq1 and self.readFilesIn.fastq2, self.ABSENT_FASTQ

        out_command = [self.PATH, self.readFilesIn_FLAG, self.readFilesIn_ARG1, self.readFilesIn_ARG2]
        for key, value in self.ARGS.items():
            if not value:
                continue
            if isinstance(value, list) or isinstance(value, set):
                out_command.append(delim.join(map(str, [key, delim.join(map(str, value))])))
            else:
                out_command.append(delim.join(map(str, [key, value])))

        out_command.append(self.outFileNamePrefix_FLAG)
        out_command.append(self.get_full_out_prefix())

        return delim.join(out_command)


    def set_readFilesIn(self, read_files_in, make_prefix=False):
        assert len(read_files_in) == 2, self.INVALID_FASTQ
        assert os.path.isfile(read_files_in[0]), self.INVALID_FASTQ
        assert os.path.isfile(read_files_in[1]), self.INVALID_FASTQ
        assert read_files_in[0] != read_files_in[1], self.INVALID_FASTQ

        self.readFilesIn_ARG1, self.readFilesIn_ARG2 = read_files_in

        if make_prefix:
            fastq1, fastq2 = basename(self.readFilesIn_ARG1), basename(self.readFilesIn_ARG2)
            prefix = ""
            i = 0
            l1, l2 = fastq1[i], fastq2[i]
            while l1 == l2:
                i += 1
                prefix += l1
                l1, l2 = fastq1[i], fastq2[i]
            if len(prefix) >= 1:
                self.outFileNamePrefix.prefix = prefix.strip('.').strip('_')

    def save_state(self):
        out_config_dict = self.econdeJSON()

        with open(self.RunSTAR.STAR_ALIGN_READS_CONFIG_PATH, 'w') as outfile:
            outfile.write(json.dumps(out_config_dict, indent=4))


    def encodeJSON(self):
        outdict = self.__dict__.copy()
        del outdict['PARSE_VERSION']
        return outdict

    def decodeJSON(self):
        pass


    def update_paths_relative(self, output_dir):
        self.OUTPUT_DIR = os.path.join(output_dir, self.OUTPUT_DIR)
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)

        self.STAR_ALIGN_READS_CONFIG_PATH = os.path.join(
            self.OUTPUT_DIR, self.STAR_ALIGN_READS_CONFIG_PATH)


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

        self.inputSam = type("PicardInputSam", (),
                             {
                                 "flag": "I",
                                 "path": None
                             })

        self.inputSam = type("PicardOutputSam", (),
                             {
                                 "flag": "O",
                                 "path": None
                             })


class RunPicardMarkDuplicates(UserRunPicardMarkDuplicates):
    def __init__(self):
        super().__init__()
