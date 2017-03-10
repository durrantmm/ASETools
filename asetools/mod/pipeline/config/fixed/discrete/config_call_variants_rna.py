#!/usr/bin/env python3
from collections import OrderedDict
import os, sys
from os.path import basename, dirname
from recordclass import recordclass
from config.custom import *
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
        self.RunAddReadGroups = RunAddReadGroups()
        self.RunMarkDuplicates = RunMarkDuplicates()

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
        self.RunMarkDuplicates.update_paths_relative(self.MAIN_OUTPUT_DIR)


    def update_paths_relative(self, output_dir):
        self.output_dir = os.path.join(output_dir, self.output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

        self.json_path = os.path.join(
            self.output_dir, self.json_path)


class RunAddReadGroups(UserRunAddReadGroups):

    def __init__(self):
        super().__init__()
        self.output_dir = "STEP2_add_read_groups"
        self.json_path = 'RunAddReadGroups.json'

        self.parse_java_version = lambda x: x.decode(STR_CONST.UTF8).split()[2].strip('\"')
        self.JAVA_VERSION_ERROR = "Your java is version {ACTUAL}, not {EXPECTED}, as specified in the config file."

        self.parse_version = lambda x: x.decode(STR_CONST.UTF8).split()[x.decode(STR_CONST.UTF8).split().index(self.VERSION)]
        self.VERSION_ERROR = "Your Picard is version {ACTUAL}, not {EXPECTED}, as specified in the config file."

        self.ABSENT_INPUT_OUTPUT = "You are missing an input and an output file for AddOrReplaceReadGroups"
        self.ARGUMENT_TYPE_ERROR = "All flags and arguments must be strings or ints"

        inputFileClass = recordclass('inputFile', 'flag, path, suffix')
        self.input_file = inputFileClass(flag="I", path=None, suffix='.sam')

        outputFileClass = recordclass('outputFile', 'flag, path, suffix')
        self.output_file = outputFileClass(flag="O", path=None, suffix='.RG.bam')

        self.FLAG_ARG_DELIM = "="


    def format_command_args(self, delim=STR_CONST.SPACE):
        assert self.input_file.path and self.output_file.path, self.ABSENT_INPUT_OUTPUT

        out_command = [self.PATH, self.FLAG_ARG_DELIM.join([self.input_file.flag, self.input_file.path]),
                       self.FLAG_ARG_DELIM.join([self.output_file.flag, self.output_file.path])]

        for key, value in self.ARGS.items():
            if not value:
                continue
            assert isinstance(value, str) and not isinstance(value, int), self.ARGUMENT_TYPE_ERROR

            out_command.append(self.FLAG_ARG_DELIM.join(map(str, [key, value])))

        return delim.join(out_command)


    def adjust_input_output_RunSTAR(self, RunSTAR_json):
        global STR_CONST
        if self.input_file.path and self.output_file.path:
            return
        if not self.input_file.path:
            input_path = adjust_path_relative(dirname(self.output_dir), RunSTAR_json['output_sam'])
            assert input_path.endswith(self.input_file.suffix), \
                'The input file for AddOrReplaceReadGroups must end in %s' % self.input_file.suffix
            self.input_file.path = input_path
        if not self.output_file.path:
            output_prefix = basename(RunSTAR_json['outFileNamePrefix']['prefix'])
            out_prefix = os.path.join(self.output_dir, output_prefix)
            self.output_file.path = STR_CONST.EMPTY_STRING.join([out_prefix, self.output_file.suffix])


    def update_paths_relative(self, output_dir):
        self.output_dir = os.path.join(output_dir, self.output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

        self.run_add_groups_json_path = os.path.join(
            self.output_dir, self.json_path)


    def set_input(self, input_path):
        self.input.path = os.path.abspath(input_path)


    def get_json_path(self):
        return os.path.join(self.output_dir, self.json_path)


class RunMarkDuplicates(UserRunMarkDuplicates):

    def __init__(self):
        super().__init__()
        self.output_dir = "STEP3_mark_duplicates"
        self.json_path = 'RunMarkDuplicates.json'

        self.parse_java_version = lambda x: x.decode(STR_CONST.UTF8).split()[2].strip('\"')
        self.JAVA_VERSION_ERROR = "Your java is version {ACTUAL}, not {EXPECTED}, as specified in the config file."

        self.parse_version = lambda x: x.decode(STR_CONST.UTF8).split()[x.decode(STR_CONST.UTF8).split().index(self.VERSION)]
        self.VERSION_ERROR = "Your Picard is version {ACTUAL}, not {EXPECTED}, as specified in the config file."

        self.ABSENT_INPUT_OUTPUT = "You are missing an input and an output file for MarkDuplicates."
        self.ARGUMENT_TYPE_ERROR = "All flags and arguments must be strings or ints."

        inputFileClass = recordclass('inputFile', 'flag, path, suffix')
        self.input_file = inputFileClass(flag="I", path=None, suffix='.RG.bam')

        outputFileClass = recordclass('outputFile', 'flag, path, suffix')
        self.output_file = outputFileClass(flag="O", path=None, suffix='.RG.MD.bam')

        self.FLAG_ARG_DELIM = "="


    def format_command_args(self, delim=STR_CONST.SPACE):
        assert self.input_file.path and self.output_file.path, self.ABSENT_INPUT_OUTPUT

        out_command = [self.PATH, self.FLAG_ARG_DELIM.join([self.input_file.flag, self.input_file.path]),
                       self.FLAG_ARG_DELIM.join([self.output_file.flag, self.output_file.path])]

        for key, value in self.ARGS.items():
            if not value:
                continue
            assert isinstance(value, str) and not isinstance(value, int), self.ARGUMENT_TYPE_ERROR

            out_command.append(self.FLAG_ARG_DELIM.join(map(str, [key, value])))

        return delim.join(out_command)


    def adjust_input_output_RunAddReadGroups(self, RunAddReadGroups_json):
        global STR_CONST

        if self.input_file.path and self.output_file.path:
            return

        if not self.input_file.path:
            input_path = adjust_path_relative(dirname(self.output_dir), RunAddReadGroups_json['output_file']['path'])
            assert input_path.endswith(self.input_file.suffix), \
                'The input file for MarkDuplicates must end in %s' % self.input_file.suffix
            self.input_file.path = input_path

        if not self.output_file.path:
            output_path_prefix = remove_suffix(basename(RunAddReadGroups_json['output_file']['path'],
                                                        RunAddReadGroups_json['output_file']['suffix']))
            out_prefix = os.path.join(self.output_dir, output_path_prefix)
            self.output_file.path = STR_CONST.EMPTY_STRING.join([out_prefix, self.output_file.suffix])


    def update_paths_relative(self, output_dir):
        self.output_dir = os.path.join(output_dir, self.output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

        self.run_add_groups_json_path = os.path.join(
            self.output_dir, self.json_path)

    def set_input(self, input_path):
        self.input.path = os.path.abspath(input_path)

    def get_json_path(self):
        return os.path.join(self.output_dir, self.json_path)


def adjust_path_relative(relative_path, path):
    path = antijoin_paths(relative_path, path)
    return os.path.join(relative_path, path)


def antijoin_paths(short_path, long_path):
    long_path_split = long_path.split(os.sep)
    trimmed_path = []
    for elem in reversed(long_path_split):
        if elem == '':
            continue
        elif trimmed_path == []:
            trimmed_path = [elem] + trimmed_path
        elif not os.path.isfile(os.path.join(short_path, os.sep.join(trimmed_path))):
            trimmed_path = [elem] + trimmed_path
        else:
            break

    return os.sep.join(trimmed_path)


def remove_suffix(string, suffix):
    if string.endswith(suffix):
        return ''.join(list.string[:-len(suffix)])
    else:
        return string
