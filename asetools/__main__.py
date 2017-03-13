#!/usr/bin/env python3
import argparse, os, sys

from mod.misc.string_constants import *
from mod.misc.log import Log
from mod.qsub import QSubmit
from mod.pipeline.run.piped.rnaseq_variant_calling import RunRNASeqVariantCalling

PIPELINE_SUBPARSER_STR = 'pipeline'
ANALYSIS_SUBPARSER_STR = 'analysis'

PIPELINE_NAME_STR = 'pipeline_name'

RNASEQ_VARIANT_CALLER_STR = 'RNAseqVariantCaller'

OUTPUT_DIR_STR = 'output_dir'
FASTQ1_FLAG = '--fastq1'
FASTQ2_FLAG = '--fastq2'

QSUB_FLAG = '--qsub'


def main(args):
    os.makedirs(args.output_dir, exist_ok=True)
    if args.pipeline_or_analysis==PIPELINE_SUBPARSER_STR:

        if args.pipeline_name==RNASEQ_VARIANT_CALLER_STR:
            if args.qsub:

                qsub = QSubmit(args.output_dir, args.qsub, SPACE.join(sys.argv))
                qsub.submit()

            else:

                rnaseq_var_caller = RunRNASeqVariantCalling(output_dir=args.output_dir,
                                                            fastq1=args.fastq1,
                                                            fastq2=args.fastq2,
                                                            logger=Log(args.output_dir))
                rnaseq_var_caller.run()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='Specify if you want to run a pipeline or a specific analysis',
                                       dest='pipeline_or_analysis')
    subparsers.required = True
    pipeline_parser = subparsers.add_parser(PIPELINE_SUBPARSER_STR)
    analysis_parser = subparsers.add_parser(ANALYSIS_SUBPARSER_STR)

    pipeline_subparsers = pipeline_parser.add_subparsers(help="Specify which pipeline you'd like to run.'",
                                                         dest=PIPELINE_NAME_STR)
    pipeline_subparsers.required = True
    rnaseq_var_call_pipeline = pipeline_subparsers.add_parser(RNASEQ_VARIANT_CALLER_STR)

    rnaseq_var_call_pipeline.add_argument(OUTPUT_DIR_STR)
    rnaseq_var_call_pipeline.add_argument(FASTQ1_FLAG, required=True)
    rnaseq_var_call_pipeline.add_argument(FASTQ2_FLAG, required=True)
    rnaseq_var_call_pipeline.add_argument(QSUB_FLAG)

    args = parser.parse_args()
    main(args)