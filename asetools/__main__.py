#!/usr/bin/env python3
import argparse
import os
import sys

from mod.process.run_python.vcf_filter_ase import RunVCFFilterASE

from mod.misc.log import Log
from mod.misc.string_constants import *
from mod.process.get_reference_bases import RunGetReferenceBases
from mod.qsub import QSubmit
from mod.subprocess.run_process import RunRNASeqVariantCalling
from mod.subprocess.run_process import WASPAlleleSpecificExpressionPipeline

# Important strings used to parse the input
PIPELINE_SUBPARSER_STR = 'subprocess'
ANALYSIS_SUBPARSER_STR = 'process'

PIPELINE_NAME_STR = 'pipeline_name'
ANALYSIS_NAME_STR = 'analysis_name'

RNASEQ_VARIANT_CALLER_STR = 'RNAseqVariantCaller'
WASP_ASE_READ_COUNTER_STR = 'WASP-ASEReadCounter'

VCF_FILTER_ASE_STR = 'VCFFilterASE'
GET_REF_BASES_STR = 'GetReferenceBases'

OUTPUT_DIR_STR = 'output_dir'
FASTQ1_FLAG = '--fastq1'
FASTQ2_FLAG = '--fastq2'
BAM_FLAG = '--bam'
VCF_FLAG = '--vcf'
TSV_FLAG = '--vcf'

CHROM_COL_FLAG = '--chrom-col'
POS_COL_FLAG = '--position-col'

QSUB_FLAG = '--qsub'


def main(args):
    """
    This is the main function that carries out all of the arguments passed to the __main__.py script.
    :param args: The arguments passed in through the command line and parsed with argparse
    :return:
    """
    # Make the main directory that will be used to output all of the information.
    os.makedirs(args.output_dir, exist_ok=True)

    # This checks to see if the user chose the RNAseq Variant Calling Pipeline
    if args.pipeline_name==RNASEQ_VARIANT_CALLER_STR:

        # This code turns a command line request into a sungrid engine submission
        # script so that it can quickly be submitted to a computing cluster.
        if args.qsub:

            qsub = QSubmit(args.output_dir, args.qsub, SPACE.join(sys.argv))
            qsub.submit()

        # Otherwise, it performs the process without submitting it to the cluster.
        else:

            rnaseq_var_caller = RunRNASeqVariantCalling(output_dir=args.output_dir,
                                                        fastq1=args.fastq1,
                                                        fastq2=args.fastq2,
                                                        logger=Log(args.output_dir))
            rnaseq_var_caller.run()

    # This executes the WASP ASE read coutning subprocess if selected
    elif args.pipeline_name==WASP_ASE_READ_COUNTER_STR:

        # Submit the job to the cluster
        if args.qsub:
            qsub = QSubmit(args.output_dir, args.qsub, SPACE.join(sys.argv))
            qsub.submit()

        # Or run it locally without submitting it to the cluster.
        else:

            wasp_pipeline = WASPAlleleSpecificExpressionPipeline(output_dir=args.output_dir,
                                                                 input_bam=args.bam,
                                                                 input_vcf=args.vcf,
                                                                 logger=Log(args.output_dir))
            wasp_pipeline.run()



    if args.analysis_name == VCF_FILTER_ASE_STR:

        filter_vcf = RunVCFFilterASE(output_dir=args.output_dir,
                                     input_vcf=args.vcf,
                                     logger=Log(args.output_dir))
        filter_vcf.run()

    elif args.analysis_name == GET_REF_BASES_STR:

        get_ref_bases = RunGetReferenceBases(output_dir=args.output_dir,
                                             input_tsv=args.tsv,
                                             logger=Log(args.output_dir))





def parse_arguments():

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='subprocess',
                                       dest='script_name')
    subparsers.required = True

    ### ARGUMENTS FOR THE RNASEQ VARIANT CALLER PIPELINE
    rnaseq_var_call_pipeline = subparsers.add_parser(RNASEQ_VARIANT_CALLER_STR)

    rnaseq_var_call_pipeline.add_argument(OUTPUT_DIR_STR)
    rnaseq_var_call_pipeline.add_argument(FASTQ1_FLAG, required=True)
    rnaseq_var_call_pipeline.add_argument(FASTQ2_FLAG, required=True)
    rnaseq_var_call_pipeline.add_argument(QSUB_FLAG)

    # WASP PIPELINE
    wasp_pipeline = subparsers.add_parser(WASP_ASE_READ_COUNTER_STR)
    wasp_pipeline.add_argument(OUTPUT_DIR_STR)
    wasp_pipeline.add_argument(BAM_FLAG, required=True)
    wasp_pipeline.add_argument(VCF_FLAG, required=True)
    wasp_pipeline.add_argument(QSUB_FLAG)

    # VCF ase filtration
    vcf_ase_filter = subparsers.add_parser(VCF_FILTER_ASE_STR)
    vcf_ase_filter.add_argument(OUTPUT_DIR_STR)
    vcf_ase_filter.add_argument(VCF_FLAG, required=True)


    # Get Reference Bases
    get_reference_bases = subparsers.add_parser(GET_REF_BASES_STR)
    get_reference_bases.add_argument(OUTPUT_DIR_STR)
    get_reference_bases.add_argument(TSV_FLAG, required=True)
    get_reference_bases.add_argument(CHROM_COL_FLAG, type=int, default=1)
    get_reference_bases.add_argument(POS_COL_FLAG, type=int, default=1)


    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_arguments()

    main(args)