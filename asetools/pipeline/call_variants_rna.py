#!/usr/bin/env python3
import sys, os
import subprocess
import argparse
import json
from config.config_call_variants_rna import CallVariantsRNAConfig
from config.log import Log
from config import save_config

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

    if run_pipeline_step(pipeline_start, PICARD_ADD_OR_REPLACE_READ_GROUPS, pipeline_order):
        add_read_groups_picard(config, log)


def align_reads_STAR(config, log=None):
    global STR_CONST
    #check_version(config.RunSTAR.PATH, config.RunSTAR.VERSION_FLAG, config.RunSTAR.VERSION,
    #              config.RunSTAR.PARSE_VERSION, config.RunSTAR.VERSION_ERROR)
    if log: log.info("STAR is the correct version...")
    star_command_args = config.RunSTAR.format_command_args()

    if log:
        log.info("Running STAR aligner on the provided fastq files...")
        log.info("Command used to run STAR Aligner:"+STR_CONST.NEW_LINE+star_command_args)

    #subprocess.check_output(star_command_args.split()).decode(STR_CONST.UTF8).strip()

    config.RunSTAR.save_output_sam()
    save_config.RunSTAR.save(config.RunSTAR)
    if log: log.info("Finished running STAR, everything went well...")


def add_read_groups_picard(config, log):
    global STR_CONST
    config.RunAddReadGroups.adjust_input_output_RunSTAR(save_config.read_json_to_dict(config.RunSTAR.get_json_path()))

    check_version(config.RunAddReadGroups.JAVA_PATH, config.RunAddReadGroups.JAVA_VERSION_FLAG,
                  config.RunAddReadGroups.JAVA_VERSION, config.RunAddReadGroups.parse_java_version,
                  config.RunAddReadGroups.JAVA_VERSION_ERROR, stdout=subprocess.STDOUT)
    if log: log.info("Java version is correct...")

    check_version(config.RunAddReadGroups.PATH, config.RunAddReadGroups.VERSION_FLAG, config.RunAddReadGroups.VERSION,
                  config.RunAddReadGroups.parse_version, config.RunAddReadGroups.VERSION_ERROR,
                  stdout=subprocess.STDOUT, ignore_error=True)
    if log: log.info("Picard version is correct...")

    add_read_groups_command = config.RunAddReadGroups.format_command_args()
    # subprocess.check_output(star_command_args.split()).decode(STR_CONST.UTF8).strip()





def run_pipeline_step(start, step, order):
    if order.index(start) <= order.index(step):
        return True
    else:
        return False


def check_version(app_path, version_flag, version, parse_version, version_error, stdout=subprocess.PIPE, ignore_error=False):
    try:
        output = subprocess.check_output(app_path.split() + version_flag.split(), stderr=stdout)
    except subprocess.CalledProcessError as e:
        if ignore_error:
            output = e.output
        else:
            raise e

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


