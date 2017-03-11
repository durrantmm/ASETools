#!/usr/bin/env python3
import argparse
import os
import subprocess

from config import save_config
from config.fixed.discrete.config_call_variants_rna import CallVariantsRNAConfig
from mod.misc.log import Log

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

    if run_pipeline_step(pipeline_start, PICARD_MARK_DUPLICATES, pipeline_order):
        mark_duplicates_picard(config, log)





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
    if log:
        log.info("Running Picard AddOrReplaceReadGroups...")
        log.info("Command used to run Picard:"+STR_CONST.NEW_LINE+add_read_groups_command)
    subprocess.check_output(add_read_groups_command.split()).decode(STR_CONST.UTF8).strip()

    save_config.RunAddReadGroups.save(config.RunAddReadGroups)
    if log: log.info("Finished running Picard AddOrReplaceReadGroups, everything went well...")


def mark_duplicates_picard(config, log):
    global STR_CONST
    config.RunMarkDuplicates.adjust_input_output_RunAddReadGroups(
        save_config.read_json_to_dict(config.RunAddReadGroups.get_json_path()))

    check_version(config.RunMarkDuplicates.JAVA_PATH, config.RunMarkDuplicates.JAVA_VERSION_FLAG,
                  config.RunMarkDuplicates.JAVA_VERSION, config.RunMarkDuplicates.parse_java_version,
                  config.RunMarkDuplicates.JAVA_VERSION_ERROR, stdout=subprocess.STDOUT)
    if log: log.info("Java version is correct...")

    check_version(config.RunMarkDuplicates.PATH, config.RunMarkDuplicates.VERSION_FLAG, config.RunMarkDuplicates.VERSION,
                  config.RunMarkDuplicates.parse_version, config.RunMarkDuplicates.VERSION_ERROR,
                  stdout=subprocess.STDOUT, ignore_error=True)
    if log: log.info("Picard version is correct...")

    add_read_groups_command = config.RunMarkDuplicates.format_command_args()
    if log:
        log.info("Running Picard MarkDuplicates...")
        log.info("Command used to run Picard:"+STR_CONST.NEW_LINE+add_read_groups_command)
    subprocess.check_output(add_read_groups_command.split()).decode(STR_CONST.UTF8).strip()

    save_config.RunMarkDuplicates.save(config.RunMarkDuplicates)
    if log: log.info("Finished running Picard MarkDuplicates, everything went well...")


def run_pipeline_step(start, step, order):
    if order.index(start) <= order.index(step):
        return True
    else:
        return False


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


