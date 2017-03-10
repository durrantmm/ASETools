#!/usr/bin/env python3
import sys, os
import subprocess
import argparse
import json
from config.config_call_variants_rna import CallVariantsRNAConfig
from config.log import Log

### Global attributes and methods accessible to all classes
STR_CONST = type("StringConstants", (),
                 {'UTF8':'utf-8',
                  'EMPTY_STRING': '',
                  'NEW_LINE': '\n',
                  'SPACE': ' '})

STAR_ALIGN_READS = "align_reads"
PICARD_ADD_OR_REPLACE_READ_GROUPS = "add_read_groups"
PICARD_MARK_DUPLICATES = "mark_duplicates"


def run(config, log):
    log.info("Beginning ASETools RNASeq Variant Calling Pipeline...")
    os.makedirs(config.MAIN_OUTPUT_DIR, exist_ok=True)

    pipeline_start = config.START
    pipeline_order = config.ORDER

    if run_pipeline_step(pipeline_start, STAR_ALIGN_READS, pipeline_order):
        align_reads_STAR(config, log)
        config.RunSTAR.write_step_config(config)


def align_reads_STAR(config, log=None):
    global STR_CONST
    check_version(config.RunSTAR.PATH, config.RunSTAR.VERSION_FLAG, config.RunSTAR.VERSION,
                  config.RunSTAR.PARSE_VERSION, config.RunSTAR.VERSION_ERROR)
    star_command_args = config.RunSTAR.format_command_args()

    if log:
        log.info("Running STAR aligner on the provided fastq files...")
        log.info("Command used to run STAR Aligner:"+STR_CONST.NEW_LINE+pretty_format_command(star_command_args.split()))

    sys.exit()
    subprocess.check_output(star_command_args.split()).decode(STR_CONST.UTF8).strip()


    return config

def pretty_format_command(commands, flag_prefix='--'):
    global STR_CONST
    out_str = commands[0] + STR_CONST.NEW_LINE
    commands = commands[1:]
    for index, command in enumerate(commands):
        if command.startswith(flag_prefix) and commands[index+1].startswith(flag_prefix):
            out_str += command + STR_CONST.NEW_LINE
            continue

        if command.startswith(flag_prefix):
            out_str += command + STR_CONST.SPACE
            tmp_index = index+1
            while not commands[tmp_index].startswith(flag_prefix) and tmp_index < len(commands):
                out_str += commands[tmp_index] + STR_CONST.SPACE
                tmp_index += 1
            out_str += STR_CONST.SPACE

def run_pipeline_step(start, step, order):
    if order.index(start) <= order.index(step):
        return True
    else:
        return False


def check_version(app_path, version_flag, version, parse_version, version_error):
    output = subprocess.check_output([app_path, version_flag])
    local_version = parse_version(output)
    assert version == local_version, version_error.format(ACTUAL=local_version, EXPECTED=version)


if __name__ == "__main__":

    def argument_parser(config):

        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument('output', type=str,
                            help='The output folder to be used by the pipeline.')

        parser.add_argument('--readFilesIn', type=str, nargs=2,
                            help = "Specify the paired-end fastq files if you starting at the alignment step.")

        parser.add_argument('-s', '--start', choices=config.ORDER, type=str,
                            help="Choose the point in the call variants pipeline at which you'd like to start.")

        args = parser.parse_args()

        return args


    def set_config(config, args):
        global STR_CONST
        # Adding the override arguments
        if args.readFilesIn:
            config.RunSTAR.set_readFilesIn(args.readFilesIn, make_prefix=True)

        # Setting the start position
        if args.start:
            config.START = args.start

        # Setting the main output dir
        config.update_main_output_path(args.output)

        return config


    config = CallVariantsRNAConfig()
    args = argument_parser(config)

    set_config(config, args)

    log = Log(config.MAIN_OUTPUT_DIR)

    run(config, log)


