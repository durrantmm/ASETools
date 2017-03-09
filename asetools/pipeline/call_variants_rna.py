#!/usr/bin/env python3

import sys, os
from os.path import basename, splitext
import importlib.machinery
import subprocess
import argparse
from collections import namedtuple
from glob import glob
import json

tab = '\t'
whitespace = ' '
new_line = '\n'
utf8 = "utf-8"

STAR_ALIGN_READS = "align_reads"
PICARD_ADD_OR_REPLACE_READ_GROUPS = "add_read_groups"
PICARD_MARK_DUPLICATES = "mark_duplicates"



def run(config):

    os.makedirs(config.PipelineFlow.CallVariantsRNASeq.OUTPUT_DIR, exist_ok=True)

    pipeline_start = config.PipelineFlow.CallVariantsRNASeq.START
    pipeline_order = config.PipelineFlow.CallVariantsRNASeq.ORDER

    if run_pipeline_step(pipeline_start, STAR_ALIGN_READS, pipeline_order):
        config = align_reads_STAR(config)
        write_config_align_reads_STAR(config)

def align_reads_STAR(config):
    if config.STAR.outFileNamePrefix_ARG:
        config.STAR.outFileNamePrefix_ARG = os.path.join(config.PipelineFlow.CallVariantsRNASeq.OUTPUT_DIR,
                                                         config.STAR.outFileNamePrefix_ARG)
    else:
        config.STAR.outFileNamePrefix_ARG = os.path.join(config.PipelineFlow.CallVariantsRNASeq.OUTPUT_DIR,
                                                         basename(config.PipelineFlow.OUTPUT_DIR))

    check_version(config.STAR.PATH, config.STAR.VERSION, config.STAR.PARSE_VERSION, config.STAR.VERSION_ERROR)
    star_command_args = format_command_args(config.STAR.STAR_COMMAND_DICT)
    star_command = whitespace.join([config.STAR.PATH, star_command_args])
    subprocess.check_output(star_command.split()).decode(utf8).strip()
    return config

def write_config_align_reads_STAR(config):
    global tab, newline
    out_config = lambda: None
    out_config.output_prefix = config.STAR.outFileNamePrefix_ARG
    out_config_dict = out_config.__dict__()
    with open(config.PipelineFlow.CallVariantsRNASeq.STAR_ALIGN_READS_CONFIG_PATH, 'w') as outfile:
        outfile.write(json.dumps(out_config_dict, indent=4))



# Version Checks
def check_version(star_path, version, parse_version, version_error, version_flag="--version"):
    output = subprocess.check_output([star_path, version_flag])
    local_version = parse_version(output)
    assert version == local_version, version_error.format(ACTUAL=local_version, EXPECTED=version)


# Misc functions
def format_command_args(command_args, delim=whitespace):
    out_command = []
    for key, value in command_args.items():
        if not value:
            continue
        if isinstance(value, list) or isinstance(value, set):
            out_command.append(delim.join(map(str, [key, delim.join(map(str, value))])))
        else:
            out_command.append(delim.join(map(str, [key, value])))
    return delim.join(out_command)


def run_pipeline_step(start, step, order):
    if order.index(start) <= order.index(step):
        return True
    else:
        return False


def get_config(config_path):
    config_module_name = splitext(basename(config_path))[0]
    config = importlib.machinery.SourceFileLoader(config_module_name, config_path).load_module().Config


def dict_to_namedtuple(dict_in):
    return namedtuple('GenericDict', dict_in.keys())(**dict_in)


def adjust_config_by_args(config, args):
    # Adding the override arguments
    if args.override_star_argument:
        for entry in args.override_star_argument:
            flag, argument = entry.split()[0], whitespace.join(entry.split()[1:])
            config.StarAligner.STAR_COMMAND_DICT[flag] = argument

    # Setting the start position
    config.PipelineFlow.CallVariantsRNASeq.START = args.start

    # Setting the main output dir
    config.PipelineFlow.OUTPUT_DIR = args.output_dir

    return config


def arrange_output_dir(output_dir, config):
    config.PipelineFlow.update_main_output_path(output_dir)
    return config


def argument_parser():

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('config', type=str,
                        help='The config.py file to use in the pipeline.')
    parser.add_argument('output', type=str,
                        help='The output folder to be used by the pipeline.')
    args_first_parse = dict_to_namedtuple(vars(parser.parse_args()))
    config = get_config(args_first_parse.config)

    parser.add_argument('-oSTAR', '--override_star_argument', action="append",
                        help="Only one new argument for each time you invoke the option."
                             "Example: -oSTAR \"--readFilesIn paired_ends.1.fq.gz paired_ends.2.fq.gz\""
                             "-oSTAR \"--out1FileNamePrefix paired_end_alignment\"")

    parser.add_argument('-s', '--start', choices=config.PipelineFlow.CallVariantsRNASeq.ORDER,
                        default=config.PipelineFlow.CallVariantsRNASeq.STAR_ALIGN_READS, type=str,
                        help="Choose the point in the call variants pipeline at which you'd like to start.")

    args = dict_to_namedtuple(vars(parser.parse_args()))

    config = adjust_config_by_args(config, args)
    config = arrange_output_dir(args.output, config)

    return config

if __name__ == "__main__":
    config = argument_parser()

    run(config)


