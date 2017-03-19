"""
This module contains the RunRNASeqVariantCalling class, which is a subclass of RunPipelineSuper.

This executes the full RNAseq Variant Calling pipeline as detailed by the GATK best practices.
"""

from os.path import join

from mod.subprocess.add_read_groups import RunPicardAddReadGroups
from mod.subprocess.haplotype_caller import RunGATKHaplotypeCaller
from mod.subprocess.print_reads import RunGATKPrintReads
from mod.subprocess.rnaseq_base_recalibrator import RunGATKRNAseqBaseRecalibrator
from mod.subprocess.split_n_cigar_reads import RunGATKSplitNCigarReads
from mod.subprocess.star_align import RunStarAlign
from mod.subprocess.variant_filtration import RunGATKVariantFiltration
from mod.process.vcf_summary_statistics import RunVcfSummaryStatistics

from mod.config.fixed import RNASeqVariantCallingFixedConfig
from mod.run_pipeline_superclass import RunPipelineSuper
from mod.subprocess.mark_duplicates import RunPicardMarkDuplicates


class RunRNASeqVariantCalling(RunPipelineSuper):
    """
    This class executes the full RNAseq Variant Calling pipeline as detailed by the GATK best practices.
    """

    def __init__(self, output_dir, fastq1, fastq2, logger):
        """
        Constructor for a RunRNASeqVariantCalling object.
        :param output_dir: The output directory to save all of the output.
        :param fastq1: The first FASTQ file for the paired-end reads.
        :param fastq2: The second FASTQ files for the paired-end reads.
        :param logger: The logger to use when executing the pipeline.
        """
        fixed_config = RNASeqVariantCallingFixedConfig()

        name = fixed_config.name
        output_dir = output_dir

        input = fixed_config.input
        input.arg1 = fastq1
        input.arg2 = fastq2

        logger = logger

        super().__init__(name, output_dir, input, logger)


    def execute_steps(self):

        # STAR ALIGN
        star_output_dir = join(self.output_dir, 'STEP1_STAR_ALIGN')
        run_star = RunStarAlign(output_dir=star_output_dir,
                                fastq1=self.input.arg1,
                                fastq2=self.input.arg2,
                                logger=self.logger)
        run_star.run()
        star_output_sam = run_star.retrieve_output_path()


        # ADD READ GROUPS
        add_read_groups_output_dir = join(self.output_dir, "STEP2_ADD_READ_GROUPS")
        run_add_read_groups = RunPicardAddReadGroups(output_dir=add_read_groups_output_dir,
                                                     input_sam=star_output_sam,
                                                     logger=self.logger)
        run_add_read_groups.run()
        arg_output_bam = run_add_read_groups.retrieve_output_path()


        # MARK DUPLICATES
        mark_dups_output_dir = join(self.output_dir, "STEP3_MARK_DUPLICATES")
        mark_dups = RunPicardMarkDuplicates(output_dir = mark_dups_output_dir,
                                            input_bam=arg_output_bam,
                                            logger=self.logger)
        mark_dups.run()
        mark_dups_bam = mark_dups.retrieve_output_path()


        # SPLIT READS
        split_reads_output_dir = join(self.output_dir, "STEP4_SPLIT_READS")
        split_reads = RunGATKSplitNCigarReads(output_dir = split_reads_output_dir,
                                              input_bam=mark_dups_bam,
                                              logger=self.logger)
        split_reads.run()
        split_reads_bam = split_reads.retrieve_output_path()


        # RECALIBRATE BASES
        recal_bases_output_dir = join(self.output_dir, "STEP5_RECAL_BASES")
        recal_bases = RunGATKRNAseqBaseRecalibrator(output_dir=recal_bases_output_dir,
                                                    input_bam=split_reads_bam,
                                                    logger=self.logger)
        recal_bases.run()
        recal_table = recal_bases.retrieve_output_path()


        # PRINT READS
        print_reads_output_dir = join(self.output_dir, "STEP6_PRINT_READS")
        print_reads = RunGATKPrintReads(output_dir=print_reads_output_dir,
                                        input_bam=split_reads_bam,
                                        input_recal_table=recal_table,
                                        logger=self.logger)
        print_reads.run()
        recal_bam = print_reads.retrieve_output_path()


        # HAPLOTYPE CALLER
        haplotype_caller_output_dir = join(self.output_dir, "STEP7_HAPLOTYPE_CALLER")
        haplotype_caller = RunGATKHaplotypeCaller(output_dir=haplotype_caller_output_dir,
                                                  input_bam=recal_bam,
                                                  logger=self.logger)
        haplotype_caller.run()
        raw_vcf = haplotype_caller.retrieve_output_path()


        # VARIANT FILTRATION
        variant_filtration_output_dir = join(self.output_dir, "STEP8_VARIANT_FILTRATION")
        variant_filter = RunGATKVariantFiltration(output_dir=variant_filtration_output_dir,
                                                  input_vcf=raw_vcf,
                                                  logger=self.logger)
        variant_filter.run()
        filtered_vcf = variant_filter.retrieve_output_path()


        # Produce summary statistics of final VCF
        # This uses my own script, vcf_summary_statistics.py, to process the final VCF produced by the pipeline,
        # providing summary statistics that can be used for quality control purposes by the user.
        vcf_sum_stats_output_dir = join(self.output_dir, "STEP9_FINAL_VCF_SUMMARY_STATS")
        vcf_sum_stats = RunVcfSummaryStatistics(output_dir=vcf_sum_stats_output_dir,
                                                input_vcf=filtered_vcf,
                                                logger=self.logger)
        vcf_sum_stats.run()


