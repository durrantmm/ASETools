#!/usr/bin/env python3

"""
AUTHOR: Matt Durrant

Primary entry point for ASEtools
This script acts as a primary entry point for ASEtools.
It includes a comprehensive command-line argument parser.

You can see the details of this argument parser by typing

    python asetools --help

This script executes many of the most important functions of this package.
"""

from mod.misc.argparse_types import *
from mod.misc.log import Log
from mod.misc.qsub import QSubmit
from mod.misc.string_constants import *
from mod.pipelines.rnaseq_variant_calling import RunRNASeqVariantCalling
from mod.pipelines.wasp_ase_pipeline import RunWASPAlleleSpecificExpressionPipeline
from mod.process.change_vcf_chrom import RunChangeVcfChrom
from mod.process.fishers_exact_test import RunFishersExactTest
from mod.process.prepare_count_data import RunPrepareReadCountData
from mod.process.retrieve_mapping_distances import RunRetrieveMappingDistances
from mod.process.vcf_filter_ase import RunVcfFilterASE
from mod.process.vcf_summary_statistics import RunVcfSummaryStatistics

# Important strings used to parse the input
PIPELINE_SUBPARSER_STR = 'subprocess'
ANALYSIS_SUBPARSER_STR = 'process'


# Pipeline Names
RNASEQ_VARIANT_CALLER_STR = 'Pipeline-RNAseqVariantCaller'
WASP_ASE_READ_COUNTER_STR = 'Pipeline-ASEReadCounterWASP'

# Single process names
CHANGE_VCF_CHROM_STR = 'ChangeVcfChrom'
VCF_SUMMARY_STATISTICS_STR = 'VcfSummaryStatistics'
VCF_FILTER_ASE_STR = 'VcfFilterASE'
PREPARE_READ_COUNT_STR = 'PrepareReadCountData'
FISHERS_EXACT_TEST_STR = 'FishersExactTest'
RETRIEVE_MAPPING_DIST_STR = 'RetrieveMappingDistances'

# Flags and argument placeholders
PROTOCOL_NAME_STR = 'protocol_name'
OUTPUT_DIR_STR = 'output_dir'
FASTQ1_FLAG = '--fastq1'
FASTQ2_FLAG = '--fastq2'
BAM_FLAG = '--bam'
VCF_FLAG = '--vcf'
TSV_FLAG = '--tsv'
CASES_FLAG = '--cases'
CONTROLS_FLAG = '--controls'
READ_COUNTS_FLAG = '--read-counts'
ADD_CHR_FLAG = '--add-chr'
REMOVE_CHR_FLAG = '--remove-chr'
QSUB_FLAG = '--qsub'

# Descriptions and help strings
ASETOOLS_DESCRIPTION = "ASEtools: a command line interface for allele-specific expression pipelines and analysis."
PROTOCOL_SELECTION_HELP = 'Specify the name of the protocol you would like to execute from the available options.'
RNASEQ_VARIANT_CALLER_HELP = 'Implements the GATK RNAseq variant calling pipeline from start to finish.'
WASP_ASE_READ_COUNTER_HELP = 'Implements the WASP ASE read count pipeline from start to finish.'
CHANGE_VCF_CHROM_HELP = 'Adds or removes the "chr" prefix from all of the chromosomes in a VCF file'
VCF_SUMMARY_STATISTICS_HELP = 'Calculates summary statistics from the specified VCF.'
VCF_FILTER_ASE_HELP = 'Filters a VCF file to only include those variants that are eligible for ASE read counting.'
PREPARE_READ_COUNT_HELP = 'Takes the output of the WASP pipeline and merges cases/controls by summing read counts.'
FISHERS_EXACT_TEST_HELP = "Takes the output of {STRING} and calculates significant differential ASE through a Fisher's " \
                          "exact test. Corrects for multiple testing correction.".format(STRING=PREPARE_READ_COUNT_STR)
RETRIEVE_MAPPING_DIST_HELP = "Retrieves the mapping distances between read pairs for all variants in the input VCF."

OUTPUT_DIR_HELP = "Specify an output directory to save the output and log files."
BAM_HELP = "A binary sequence alignment file (BAM)."
VCF_HELP = "A VCF variant file."
TSV_HELP = "A tab-separated value file."
CASES_HELP = 'Read count TSV files produced by GATK ASEReadCounter. For each given treatment, input all of the relevant' \
             'read count files separated by spaces.'
CONTROLS_HELP = 'Read count TSV files produced by GATK ASEReadCounter. For each given treatment, input all of the relevant ' \
                'read count files separated by spaces.'
READ_COUNTS_HELP = 'A read counts file produced by {STRING}'.format(STRING=PREPARE_READ_COUNT_STR)
QSUB_HELP = 'Designate a template SGE submission script if you wish to run the command on the cluster.'

def main(args):
    """
    This is the main function that carries out all of the arguments passed to the __main__.py script.
    :param args: The arguments passed in through the command line and parsed with argparse
    """

    # Make the main directory that will be used to output all of the information.
    os.makedirs(args.output_dir, exist_ok=True)



    # This checks to see if the user chose the RNAseq Variant Calling Pipeline
    if args.protocol_name==RNASEQ_VARIANT_CALLER_STR:

        # This code turns a command line request into a sungrid engine job submission
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

    # This executes the WASP ASE read counting pipeline if selected
    elif args.protocol_name ==WASP_ASE_READ_COUNTER_STR:

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


    # This executes a script that changes the chromosome identifiers of a VCF file
    # This is often necessary in order to get VCF files into the correct format.
    elif args.protocol_name == CHANGE_VCF_CHROM_STR:

        # If the user gives the --add-chr argument, this sets up the script to add the 'chr' prefix to the VCF file
        if args.add_chr:
            change_vcf_chrom = RunChangeVcfChrom(output_dir=args.output_dir,
                                                 input_vcf=args.vcf,
                                                 add_chr=True,
                                                 logger=Log(args.output_dir))

        # If the user gives the --remove-chr argument, this sets up the script to remove the 'chr' prefix
        # from the VCF file.
        elif args.remove_chr:
            change_vcf_chrom = RunChangeVcfChrom(output_dir=args.output_dir,
                                                 input_vcf=args.vcf,
                                                 add_chr=False,
                                                 logger=Log(args.output_dir))
        # Catch an argument error
        else:
            raise argparse.ArgumentTypeError('You must specify either --add-chr or --remove-chr')

        change_vcf_chrom.run()

    # This executes a scripts that gathers summary statistics about a VCF file.
    # This is useful for quality-control purposes.
    elif args.protocol_name == VCF_SUMMARY_STATISTICS_STR:
        vcf_sum_stats = RunVcfSummaryStatistics(output_dir=args.output_dir,
                                                input_vcf=args.vcf,
                                                logger=Log(args.output_dir))
        vcf_sum_stats.run()

    # This filters a VCF file to include only those reads that are relevant to allele-specific expression.
    elif args.protocol_name == VCF_FILTER_ASE_STR:

        filter_vcf = RunVcfFilterASE(output_dir=args.output_dir,
                                     input_vcf=args.vcf,
                                     logger=Log(args.output_dir))
        filter_vcf.run()


    # This prepares a collection of read count files produced by GATK ASEReadCounter
    # for the FishersExactTest protocol
    elif args.protocol_name == PREPARE_READ_COUNT_STR:

        prepare_read_counts = RunPrepareReadCountData(output_dir=args.output_dir,
                                                      cases_paths=args.cases,
                                                      controls_paths=args.controls,
                                                      logger=Log(args.output_dir))
        prepare_read_counts.run()

    # This executes the Fishers exact test protocol
    elif args.protocol_name == FISHERS_EXACT_TEST_STR:

        fishers_exact_test = RunFishersExactTest(output_dir=args.output_dir,
                                                 read_count_data=args.read_counts,
                                                 logger=Log(args.output_dir))
        fishers_exact_test.run()

    # This retrieves the mapping distance between reads.
    elif args.protocol_name == RETRIEVE_MAPPING_DIST_STR:

        retrieve_mapping_distances = RunRetrieveMappingDistances(output_dir=args.output_dir,
                                                                 input_bam=args.bam,
                                                                 input_vcf=args.vcf,
                                                                 logger=Log(args.output_dir))
        retrieve_mapping_distances.run()


def parse_arguments():

    parser = argparse.ArgumentParser(description=ASETOOLS_DESCRIPTION)

    subparsers = parser.add_subparsers(help=PROTOCOL_SELECTION_HELP,
                                       dest=PROTOCOL_NAME_STR)
    subparsers.required = True

    ### ARGUMENTS FOR THE RNASEQ VARIANT CALLER PIPELINE
    rnaseq_var_call_pipeline = subparsers.add_parser(RNASEQ_VARIANT_CALLER_STR, help=RNASEQ_VARIANT_CALLER_HELP)

    rnaseq_var_call_pipeline.add_argument(OUTPUT_DIR_STR)
    rnaseq_var_call_pipeline.add_argument(FASTQ1_FLAG, required=True)
    rnaseq_var_call_pipeline.add_argument(FASTQ2_FLAG, required=True)
    rnaseq_var_call_pipeline.add_argument(QSUB_FLAG, help=QSUB_HELP)


    # WASP ASE READ COUNTING PIPELINE
    wasp_pipeline = subparsers.add_parser(WASP_ASE_READ_COUNTER_STR, help=WASP_ASE_READ_COUNTER_HELP)
    wasp_pipeline.add_argument(OUTPUT_DIR_STR, help=OUTPUT_DIR_HELP)
    wasp_pipeline.add_argument(BAM_FLAG, required=True, help=BAM_HELP)
    wasp_pipeline.add_argument(VCF_FLAG, required=True, help=VCF_HELP)
    wasp_pipeline.add_argument(QSUB_FLAG, help=QSUB_HELP)


    # Change VCF chromosome tag
    change_vcf_chrom = subparsers.add_parser(CHANGE_VCF_CHROM_STR, help=CHANGE_VCF_CHROM_HELP)
    change_vcf_chrom.add_argument(OUTPUT_DIR_STR, help=OUTPUT_DIR_HELP)
    change_vcf_chrom.add_argument(VCF_FLAG, required=True, help=VCF_HELP)
    add_remove_chr = change_vcf_chrom.add_mutually_exclusive_group(required=True)
    add_remove_chr.add_argument(ADD_CHR_FLAG, action='store_true')
    add_remove_chr.add_argument(REMOVE_CHR_FLAG, action='store_true')

    # VCF summary statistics
    vcf_summary_stats = subparsers.add_parser(VCF_SUMMARY_STATISTICS_STR, help=VCF_SUMMARY_STATISTICS_HELP)
    vcf_summary_stats.add_argument(OUTPUT_DIR_STR, help=OUTPUT_DIR_HELP)
    vcf_summary_stats.add_argument(VCF_FLAG, required=True, help=VCF_HELP)


    # VCF ase filtration
    vcf_ase_filter = subparsers.add_parser(VCF_FILTER_ASE_STR, help=VCF_FILTER_ASE_HELP)
    vcf_ase_filter.add_argument(OUTPUT_DIR_STR, help=OUTPUT_DIR_HELP)
    vcf_ase_filter.add_argument(VCF_FLAG, required=True, help=VCF_HELP)


    # Prepare Read Count Data
    prepare_read_count_data = subparsers.add_parser(PREPARE_READ_COUNT_STR, help=PREPARE_READ_COUNT_HELP)
    prepare_read_count_data.add_argument(OUTPUT_DIR_STR, help=OUTPUT_DIR_HELP)
    prepare_read_count_data.add_argument(CASES_FLAG, type=str, nargs='+', required=True, action='append', help=CASES_HELP)
    prepare_read_count_data.add_argument(CONTROLS_FLAG, type=str, nargs='+', required=True, action='append', help=CONTROLS_HELP)


    # Fishers exact test on read count data
    fishers_exact_test = subparsers.add_parser(FISHERS_EXACT_TEST_STR, help=FISHERS_EXACT_TEST_HELP)
    fishers_exact_test.add_argument(OUTPUT_DIR_STR, help=OUTPUT_DIR_HELP)
    fishers_exact_test.add_argument(READ_COUNTS_FLAG, required=True, help=READ_COUNTS_HELP)


    # Retrieve mapping distances arguments
    retrieve_mapping_dist = subparsers.add_parser(RETRIEVE_MAPPING_DIST_STR, help=RETRIEVE_MAPPING_DIST_HELP)
    retrieve_mapping_dist.add_argument(OUTPUT_DIR_STR, help=OUTPUT_DIR_HELP)
    retrieve_mapping_dist.add_argument(BAM_FLAG, help=BAM_HELP)
    retrieve_mapping_dist.add_argument(VCF_FLAG, help=VCF_HELP)

    args = parser.parse_args()

    try:
        cases_controls(args.cases, args.controls)
    except AttributeError:
        pass

    return args


if __name__ == '__main__':

    args = parse_arguments()

    main(args)