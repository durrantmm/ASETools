#!/usr/bin/env python3
from collections import OrderedDict
import os, sys
from os.path import basename
from recordclass import recordclass
from config.user_config import *
from glob import glob

### Global attributes and methods accessible to all classes
STR_CONST = type("StringConstants", (),
                 {'UTF8':'utf-8',
                  'EMPTY_STRING': '',
                  'SPACE': ' '})


class CallVariantsRNAConfig:
    def __init__(self):
        self.name = 'CallVariantsRNAConfig'

        self.MAIN_OUTPUT_DIR = None

        self.RunSTAR = RunSTAR()
        self.RunAddReadGroups = RunPicardAddOrReplaceReadGroups()

        self.STAR_ALIGN_READS = "align_reads"
        self.PICARD_ADD_OR_REPLACE_READ_GROUPS = "add_read_groups"
        self.PICARD_MARK_DUPLICATES = "mark_duplicates"

        self.ORDER = [self.STAR_ALIGN_READS, self.PICARD_ADD_OR_REPLACE_READ_GROUPS, self.PICARD_MARK_DUPLICATES]
        self.START = self.STAR_ALIGN_READS


    def update_main_output_path(self, path):
        self.MAIN_OUTPUT_DIR = os.path.abspath(path)
        os.makedirs(self.MAIN_OUTPUT_DIR, exist_ok=True)

        self.RunSTAR.update_paths_relative(self.MAIN_OUTPUT_DIR)
        self.RunAddReadGroups.update_paths_relative(self.MAIN_OUTPUT_DIR)


class RunSTAR(UserRunSTAR):

    def __init__(self):
        super().__init__()
        self.name = 'RunSTAR'
        self.output_dir = "STEP1_STAR_alignment"

        self.run_star_json_path = "RunSTAR.json"

        self.parse_version = lambda x: x.decode(STR_CONST.UTF8).strip()
        self.VERSION_ERROR = "The STAR aligner is version {ACTUAL}, not {EXPECTED}, as specified in the config file."
        self.INVALID_FASTQ = "At least one of the fastq files you provided is invalid."
        self.ABSENT_FASTQ = "If you are running the call variants pipeline from the read alignment step, you must " \
                            "provide valid fastq files with the --readFilesIn command"

        readFilesInClass = recordclass('readFilesIn', 'flag fastq1 fastq2')
        self.readFilesIn = readFilesInClass(flag='--readFilesIn', fastq1=None, fastq2=None)

        outFileNamePrefixClass = recordclass('outFileNamePrefix', 'flag, prefix')
        self.outFileNamePrefix = outFileNamePrefixClass(flag='--outFileNamePrefix', prefix='STAR_alnmn')

        self.output_sam = None
        self.INVALID_OUTPUT_SAM_ERROR = "The sam file output by the STAR aligner cannot be found."


    def save_output_sam(self):
        output_sam = glob(self.get_full_out_prefix() + '*.sam')
        assert len(output_sam) == 1, self.INVALID_OUTPUT_SAM_ERROR
        self.output_sam = output_sam.pop()


    def get_full_out_prefix(self):
        return os.path.join(self.output_dir, self.outFileNamePrefix.prefix)


    def get_json_path(self):
        return os.path.join(self.output_dir, self.run_star_json_path)


    def format_command_args(self, delim=STR_CONST.SPACE):

        assert self.readFilesIn.fastq1 and self.readFilesIn.fastq2, self.ABSENT_FASTQ

        out_command = [self.PATH, self.readFilesIn.flag, self.readFilesIn.fastq1, self.readFilesIn.fastq2]
        for key, value in self.ARGS.items():
            if not value:
                continue
            if isinstance(value, list) or isinstance(value, set):
                out_command.append(delim.join(map(str, [key, delim.join(map(str, value))])))
            else:
                out_command.append(delim.join(map(str, [key, value])))

        out_command.append(self.outFileNamePrefix.flag)
        out_command.append(self.get_full_out_prefix())

        return delim.join(out_command)


    def set_readFilesIn(self, read_files_in, make_prefix=False):
        assert len(read_files_in) == 2, self.INVALID_FASTQ
        assert os.path.isfile(read_files_in[0]), self.INVALID_FASTQ
        assert os.path.isfile(read_files_in[1]), self.INVALID_FASTQ
        assert read_files_in[0] != read_files_in[1], self.INVALID_FASTQ

        self.readFilesIn.fastq1, self.readFilesIn.fastq2 = read_files_in

        if make_prefix:
            fastq1, fastq2 = basename(self.readFilesIn.fastq1), basename(self.readFilesIn.fastq2)
            prefix = ""
            i = 0
            l1, l2 = fastq1[i], fastq2[i]
            while l1 == l2:
                i += 1
                prefix += l1
                l1, l2 = fastq1[i], fastq2[i]
            if len(prefix) >= 1:
                self.outFileNamePrefix.prefix = prefix.strip('.').strip('_')


    def update_paths_relative(self, output_dir):
        self.output_dir = os.path.join(output_dir, self.output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

        self.run_star_json_path = os.path.join(
            self.output_dir, self.run_star_json_path)


class RunPicardAddOrReplaceReadGroups(UserRunPicardAddOrReplaceReadGroups):
    def __init__(self):
        super().__init__()
        self.output_dir = "STEP2_add_read_groups"
        self.run_add_groups_json_path = 'RunPicardAddOrReplaceReadGroups.json'

        self.parse_java_version = lambda x: x.decode(STR_CONST.UTF8).split()[2].strip('\"')
        self.JAVA_VERSION_ERROR = "Your java is version {ACTUAL}, not {EXPECTED}, as specified in the config file."

        self.parse_version = lambda x: x.decode(STR_CONST.UTF8).split()[x.decode(STR_CONST.UTF8).split().index(self.VERSION)]
        self.VERSION_ERROR = "Your Picard is version {ACTUAL}, not {EXPECTED}, as specified in the config file."

        inputFileClass = recordclass('inputFile', 'flag, path, suffix')
        self.input_file = inputFileClass(flag="I", path=None, suffix='.sam')

        outputFileClass = recordclass('outputFile', 'flag, path, suffix')
        self.output_file = outputFileClass(flag="0", path=None, suffix='.bam')

        self.FLAG_ARG_DELIM = "="


    def format_command_args(self, delim=STR_CONST.SPACE):
        assert self.readFilesIn.fastq1 and self.readFilesIn.fastq2, self.ABSENT_FASTQ

        out_command = [self.PATH, self.readFilesIn.flag, self.readFilesIn.fastq1, self.readFilesIn.fastq2]
        for key, value in self.ARGS.items():
            if not value:
                continue
            if isinstance(value, list) or isinstance(value, set):
                out_command.append(delim.join(map(str, [key, delim.join(map(str, value))])))
            else:
                out_command.append(delim.join(map(str, [key, value])))

        out_command.append(self.outFileNamePrefix.flag)
        out_command.append(self.get_full_out_prefix())

        return delim.join(out_command)


    def retrieve_input_output_from_RunSTAR(self, RunSTAR_json):
        global STR_CONST
        if self.input_file.path and self.output.path:
            return
        if not self.input_file.path:
            input_path = RunSTAR_json['output_sam']
            assert input_path.endswith(self.input.suffix), \
                'The input file for AddOrReplaceReadGroups must end in %s' % self.input.suffix
            self.input_file.path = input_path
        if not self.output_file.path:
            output_prefix = basename(RunSTAR_json['outFileNamePrefix']['prefix'])
            out_prefix = os.path.join(self.output_dir, output_prefix)
            self.output_file.path = STR_CONST.EMPTY_STRING.join([out_prefix, self.output_file.suffix])


    def update_paths_relative(self, output_dir):
        self.output_dir = os.path.join(output_dir, self.output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

        self.run_add_groups_json_path = os.path.join(
            self.output_dir, self.run_add_groups_json_path)



    def set_input(self, input_path):
        self.input.path = os.path.abspath(input_path)



class RunPicardMarkDuplicates(UserRunPicardMarkDuplicates):
    def __init__(self):
        super().__init__()
