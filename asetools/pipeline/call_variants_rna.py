#!/usr/bin/env python3
import sys, os
import subprocess
import argparse
import json
from config.fixed_config import Config


### Global attributes and methods accessible to all classes
STR_CONST = type("StringConstants", (),
                 {'UTF8':'utf-8',
                  'EMPTY_STRING': '',
                  'NEW_LINE': '\n',
                  'SPACE': ' '})

STAR_ALIGN_READS = "align_reads"
PICARD_ADD_OR_REPLACE_READ_GROUPS = "add_read_groups"
PICARD_MARK_DUPLICATES = "mark_duplicates"


def run(config):

    os.makedirs(config.PipelineFlow.CallVariantsRNASeq.OUTPUT_DIR, exist_ok=True)

    pipeline_start = config.PipelineFlow.CallVariantsRNASeq.START
    pipeline_order = config.PipelineFlow.CallVariantsRNASeq.ORDER

    if run_pipeline_step(pipeline_start, STAR_ALIGN_READS, pipeline_order):
        align_reads_STAR(config)
        write_config_align_reads_STAR(config)


def align_reads_STAR(config):
    global STR_CONST

    check_version(config.RunSTAR.PATH, config.RunSTAR.VERSION, config.RunSTAR.PARSE_VERSION, config.RunSTAR.VERSION_ERROR)
    star_command_args = config.RunSTAR.format_command_args(config.PipelineFlow.CallVariantsRNASeq.OUTPUT_DIR)
    print(star_command_args)
    sys.exit()
    subprocess.check_output(star_command_args.split()).decode(STR_CONST.UTF8).strip()

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


def run_pipeline_step(start, step, order):
    if order.index(start) <= order.index(step):
        return True
    else:
        return False

if __name__ == "__main__":

    def argument_parser():

        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument('output', type=str,
                            help='The output folder to be used by the pipeline.')
        args_first_parse = parser.parse_args()

        parser.add_argument('-oSTAR', '--override_star_argument', action="append",
                            help="Only one new argument for each time you invoke the option."
                                 "Example: -oSTAR \"--readFilesIn paired_ends.1.fq.gz paired_ends.2.fq.gz\""
                                 "-oSTAR \"--out1FileNamePrefix paired_end_alignment\"")

        parser.add_argument('-s', '--start', choices=config.PipelineFlow.CallVariantsRNASeq.ORDER,
                            default=config.PipelineFlow.CallVariantsRNASeq.STAR_ALIGN_READS, type=str,
                            help="Choose the point in the call variants pipeline at which you'd like to start.")

        args = parser.parse_args()

        return args


    def set_config(config, args):
        global STR_CONST
        # Adding the override arguments
        if args.override_star_argument:
            for entry in args.override_star_argument:
                flag, argument = entry.split()[0], STR_CONST.SPACE.join(entry.split()[1:])
                config.RunSTAR.STAR_COMMAND_DICT[flag] = argument

        # Setting the start position
        config.PipelineFlow.CallVariantsRNASeq.START = args.start

        # Setting the main output dir
        config.PipelineFlow.update_main_output_path(args.output)
        config.PipelineFlow.OUTPUT_DIR = args.output

        return config


    args = argument_parser()
    config = Config()
    set_config(config, args)


    run(config)


