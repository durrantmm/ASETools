#!/usr/bin/env python3
import sys, os
import subprocess
import argparse
import json
from config.config_call_variants_rna import CallVariantsRNAConfig


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
    check_version(config.RunSTAR.PATH, config.RunSTAR.VERSION_FLAG, config.RunSTAR.VERSION,
                  config.RunSTAR.PARSE_VERSION, config.RunSTAR.VERSION_ERROR)
    star_command_args = config.RunSTAR.format_command_args(config.PipelineFlow.CallVariantsRNASeq.OUTPUT_DIR)
    print(star_command_args)
    sys.exit()
    subprocess.check_output(star_command_args.split()).decode(STR_CONST.UTF8).strip()

    return config


def write_config_align_reads_STAR(config):
    global tab, newline
    out_config = lambda: None
    out_config.output_prefix = config.STAR.outFileNamePrefix
    out_config_dict = out_config.__dict__()
    with open(config.PipelineFlow.CallVariantsRNASeq.STAR_ALIGN_READS_CONFIG_PATH, 'w') as outfile:
        outfile.write(json.dumps(out_config_dict, indent=4))


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

        parser.add_argument('-s', '--start', choices=config.PipelineFlow.CallVariantsRNASeq.ORDER,
                            default=config.PipelineFlow.CallVariantsRNASeq.STAR_ALIGN_READS, type=str,
                            help="Choose the point in the call variants pipeline at which you'd like to start.")

        args = parser.parse_args()

        return args


    def set_config(config, args):
        global STR_CONST
        # Adding the override arguments
        if args.readFilesIn:
            config.RunSTAR.set_readFilesIn(args.readFilesIn, make_prefix=True)

        # Setting the start position
        config.PipelineFlow.CallVariantsRNASeq.START = args.start

        # Setting the main output dir
        config.PipelineFlow.update_main_output_path(args.output)
        config.PipelineFlow.OUTPUT_DIR = args.output

        return config


    config = CallVariantsRNAConfig()
    args = argument_parser(config)

    set_config(config, args)


    run(config)


