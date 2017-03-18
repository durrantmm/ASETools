#!/usr/bin/env python3
import argparse
import os
import sys

from mod.process.vcf_filter_ase import RunVCFFilterASE

from mod.misc.log import Log
from mod.misc.argparse_types import *
from mod.misc.string_constants import *
from mod.process.get_reference_bases import RunGetReferenceBases
from mod.process.prepare_count_data import RunPrepareReadCountData
from mod.process.fishers_exact_test import RunFishersExactTest
from mod.process.retrieve_mapping_distances import RunRetrieveMappingDistances
from mod.qsub import QSubmit
from mod.subprocess.pipelines.rnaseq_variant_calling import RunRNASeqVariantCalling
from mod.subprocess.pipelines.wasp_ase_pipeline import RunWASPAlleleSpecificExpressionPipeline
from mod.subprocess.pipelines.align_rg_mdup import RunAlignAddGroupsMarkDups
from mod.subprocess.pipelines.ase_pipeline import RunAlleleSpecificExpressionPipeline

# Important strings used to parse the input
PIPELINE_SUBPARSER_STR = 'subprocess'
ANALYSIS_SUBPARSER_STR = 'process'

RNASEQ_VARIANT_CALLER_STR = 'Pipeline-RNAseqVariantCaller'
WASP_ASE_READ_COUNTER_STR = 'Pipeline-ASEReadCounterWASP'
ASE_READ_COUNTER_STR = 'Pipeline-ASEReadCounter'
ALIGN_ADDG_MARK_DUPS_STR = 'Pipeline-AlignAddGroupsMarkDups'

VCF_FILTER_ASE_STR = 'VCFFilterASE'
GET_REF_BASES_STR = 'GetReferenceBases'
PREPARE_READ_COUNT_STR = 'PrepareReadCountData'
FISHERS_EXACT_TEST_STR = 'FishersExactTest'
RETRIEVE_MAPPING_DIST_STR = 'RetrieveMappingDistances'

OUTPUT_DIR_STR = 'output_dir'
FASTQ1_FLAG = '--fastq1'
FASTQ2_FLAG = '--fastq2'
BAM_FLAG = '--bam'
VCF_FLAG = '--vcf'
TSV_FLAG = '--tsv'
REFERENCE_GENOME_FASTA_FLAG_LONG = '--reference'
REFERENCE_GENOME_FASTA_FLAG_SHORT = '-r'
CASES_FLAG = '--cases'
CONTROLS_FLAG = '--controls'
READ_COUNTS_FLAG = '--read-counts'

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
    if args.script_name==RNASEQ_VARIANT_CALLER_STR:

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

    elif args.script_name==ASE_READ_COUNTER_STR:

        # Submit the job to the cluster
        if args.qsub:
            qsub = QSubmit(args.output_dir, args.qsub, SPACE.join(sys.argv))
            qsub.submit()

        # Or run it locally without submitting it to the cluster.
        else:

            wasp_pipeline = RunAlleleSpecificExpressionPipeline(output_dir=args.output_dir,
                                                                input_bam=args.bam,
                                                                input_vcf=args.vcf,
                                                                logger=Log(args.output_dir))
            wasp_pipeline.run()

    # This executes the WASP ASE read coutning subprocess if selected
    elif args.script_name==WASP_ASE_READ_COUNTER_STR:

        # Submit the job to the cluster
        if args.qsub:
            qsub = QSubmit(args.output_dir, args.qsub, SPACE.join(sys.argv))
            qsub.submit()

        # Or run it locally without submitting it to the cluster.
        else:

            wasp_pipeline = RunWASPAlleleSpecificExpressionPipeline(output_dir=args.output_dir,
                                                                    input_bam=args.bam,
                                                                    input_vcf=args.vcf,
                                                                    logger=Log(args.output_dir))
            wasp_pipeline.run()


    elif args.script_name==ALIGN_ADDG_MARK_DUPS_STR:

        # This code turns a command line request into a sungrid engine submission
        # script so that it can quickly be submitted to a computing cluster.
        if args.qsub:

            qsub = QSubmit(args.output_dir, args.qsub, SPACE.join(sys.argv))
            qsub.submit()

        # Otherwise, it performs the process without submitting it to the cluster.
        else:

            align_add_groups_mark_dups = RunAlignAddGroupsMarkDups(output_dir=args.output_dir,
                                                                   fastq1=args.fastq1,
                                                                   fastq2=args.fastq2,
                                                                   logger=Log(args.output_dir))
            align_add_groups_mark_dups.run()


    elif args.script_name == VCF_FILTER_ASE_STR:

        filter_vcf = RunVCFFilterASE(output_dir=args.output_dir,
                                     input_vcf=args.vcf,
                                     logger=Log(args.output_dir))
        filter_vcf.run()

    elif args.script_name == GET_REF_BASES_STR:

        get_ref_bases = RunGetReferenceBases(output_dir=args.output_dir,
                                             input_tsv=args.tsv,
                                             input_reference_fasta=args.reference,
                                             logger=Log(args.output_dir))
        get_ref_bases.run()

    elif args.script_name == PREPARE_READ_COUNT_STR:

        prepare_read_counts = RunPrepareReadCountData(output_dir=args.output_dir,
                                                      cases_paths=args.cases,
                                                      controls_paths=args.controls,
                                                      logger=Log(args.output_dir))
        prepare_read_counts.run()

    elif args.script_name == FISHERS_EXACT_TEST_STR:

        fishers_exact_test = RunFishersExactTest(output_dir=args.output_dir,
                                                 read_count_data=args.read_counts,
                                                 logger=Log(args.output_dir))
        fishers_exact_test.run()

    elif args.script_name == RETRIEVE_MAPPING_DIST_STR:

        retrieve_mapping_distances = RunRetrieveMappingDistances(output_dir=args.output_dir,
                                                                 input_bam=args.bam,
                                                                 input_vcf=args.vcf,
                                                                 logger=Log(args.output_dir))
        retrieve_mapping_distances.run()


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

    # WASP ASE READ COUNTING PIPELINE
    wasp_pipeline = subparsers.add_parser(WASP_ASE_READ_COUNTER_STR)
    wasp_pipeline.add_argument(OUTPUT_DIR_STR)
    wasp_pipeline.add_argument(BAM_FLAG, required=True)
    wasp_pipeline.add_argument(VCF_FLAG, required=True)
    wasp_pipeline.add_argument(QSUB_FLAG)

    # ASE READ COUNTING PIPELINE
    ase_pipeline = subparsers.add_parser(ASE_READ_COUNTER_STR)
    ase_pipeline.add_argument(OUTPUT_DIR_STR)
    ase_pipeline.add_argument(BAM_FLAG, required=True)
    ase_pipeline.add_argument(VCF_FLAG, required=True)
    ase_pipeline.add_argument(QSUB_FLAG)

    # Align, Add read groups, mark duplicates pipeline
    align_add_groups_mark_dups = subparsers.add_parser(ALIGN_ADDG_MARK_DUPS_STR)

    align_add_groups_mark_dups.add_argument(OUTPUT_DIR_STR)
    align_add_groups_mark_dups.add_argument(FASTQ1_FLAG, required=True)
    align_add_groups_mark_dups.add_argument(FASTQ2_FLAG, required=True)
    align_add_groups_mark_dups.add_argument(QSUB_FLAG)

    # VCF ase filtration
    vcf_ase_filter = subparsers.add_parser(VCF_FILTER_ASE_STR)
    vcf_ase_filter.add_argument(OUTPUT_DIR_STR)
    vcf_ase_filter.add_argument(VCF_FLAG, required=True)


    # Get Reference Bases
    get_reference_bases = subparsers.add_parser(GET_REF_BASES_STR)
    get_reference_bases.add_argument(OUTPUT_DIR_STR)
    get_reference_bases.add_argument(TSV_FLAG, required=True)
    get_reference_bases.add_argument(REFERENCE_GENOME_FASTA_FLAG_SHORT, REFERENCE_GENOME_FASTA_FLAG_LONG, required=True)
    get_reference_bases.add_argument(CHROM_COL_FLAG, type=int, default=1)
    get_reference_bases.add_argument(POS_COL_FLAG, type=int, default=2)


    # Prepare Read Count Data
    prepare_read_count_data = subparsers.add_parser(PREPARE_READ_COUNT_STR)
    prepare_read_count_data.add_argument(OUTPUT_DIR_STR)
    prepare_read_count_data.add_argument(CASES_FLAG, type=str, nargs='+', required=True, action='append')
    prepare_read_count_data.add_argument(CONTROLS_FLAG, type=str, nargs='+', required=True, action='append')


    # Fishers exact test on read count data
    fishers_exact_test = subparsers.add_parser(FISHERS_EXACT_TEST_STR)
    fishers_exact_test.add_argument(OUTPUT_DIR_STR)
    fishers_exact_test.add_argument(READ_COUNTS_FLAG, required=True)

    # Retrieve mapping distances arguments
    retrieve_mapping_dist = subparsers.add_parser(RETRIEVE_MAPPING_DIST_STR)
    retrieve_mapping_dist.add_argument(OUTPUT_DIR_STR)
    retrieve_mapping_dist.add_argument(BAM_FLAG)
    retrieve_mapping_dist.add_argument(VCF_FLAG)

    args = parser.parse_args()

    try:
        cases_controls(args.cases, args.controls)
    except AttributeError:
        pass

    return args

if __name__ == '__main__':

    args = parse_arguments()

    main(args)