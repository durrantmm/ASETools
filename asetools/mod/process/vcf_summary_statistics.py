"""
AUTHOR: Matt Durrant

This module contains a RunProcessStepSuper subclass called RunVcfSummaryStatistics.

This script produces useful VCF summary, including the total number of indels, SNVs, multiallelic sites, and biallelic
sites. This is used at the end of the RNAseq variant calling pipeline to process the VCF files produced by calling
system applications with the subprocess module.
"""

import vcf
import os
from mod.misc.string_constants import *
from mod.process_step_superclass import RunProcessStepSuper
from collections import defaultdict


class RunVcfSummaryStatistics(RunProcessStepSuper):
    def __init__(self, output_dir, input_vcf, output_file=None, logger=None):
        """
        This is the constructor for a RunVcfSummaryStatistics object.
        :param output_dir: The output directory.
        :param input_vcf: The input VCF path.
        :param output_file: The output path.
        :param logger: The logger for tracking progress.
        """
        name = 'VcfSummaryStatistics'
        output_dir = output_dir

        input_file = input_vcf
        output_file = output_file

        log_name = 'vcf_summary_statistics.json'
        logger = logger

        super().__init__(name, output_dir, input_file, output_file, log_name, logger)

        self.RECORDS = 'record(s)'
        self.TOTAL = 'total'
        self.SNP = 'snp'
        self.INDEL = 'indel'
        self.MULTIALLELIC = 'multiallelic'
        self.BIALLELIC = 'biallelic'
        self.NUCLEOTIDE_CHANGES = 'nucleotide_changes'

    def process(self):
        """
        Iterates through VCF file, keeps track of several useful summary statstics and writes them to file.
        """

        reader = vcf.Reader(filename=self.input_file)

        full_stats = defaultdict(int)
        full_stats_nuc_changes = defaultdict(int)

        per_chrom_stats = defaultdict(lambda: defaultdict(int))
        per_chrom_nuc_changes = defaultdict(lambda: defaultdict(int))

        ordered_chroms = []

        for rec in reader:
            if rec.CHROM not in ordered_chroms:
                ordered_chroms.append(rec.CHROM)

            full_stats[self.TOTAL] += 1
            per_chrom_stats[rec.CHROM][self.TOTAL] += 1

            if rec.is_indel:
                full_stats[self.INDEL] += 1
                per_chrom_stats[rec.CHROM][self.INDEL] += 1

            if rec.is_snp:
                full_stats[self.SNP] += 1
                per_chrom_stats[rec.CHROM][self.SNP] += 1

            if len(rec.ALT) > 1:
                full_stats[self.MULTIALLELIC] += 1
                per_chrom_stats[rec.CHROM][self.MULTIALLELIC] += 1

            if len(rec.ALT) == 1:
                full_stats[self.BIALLELIC] += 1
                per_chrom_stats[rec.CHROM][self.BIALLELIC] += 1

            ref = rec.REF
            for alt in rec.ALT:
                if len(ref) == 1 and len(alt) == 1:
                    nucleotide_change = '{REF} to {ALT}'.format(REF=ref, ALT=alt)
                    full_stats_nuc_changes[nucleotide_change] += 1
                    per_chrom_nuc_changes[rec.CHROM][nucleotide_change] += 1

        # Begin writing results to file.
        with open(os.path.join(self.output_dir, self.output), w) as outfile:
            outfile.write("TOTAL SUMMARY STATISTICS" + NL)
            outfile.write(TAB + self.TOTAL + SPACE + self.RECORDS + SEMI + SPACE + str(full_stats[self.TOTAL]) + NL)
            outfile.write(TAB + self.SNP + SPACE + self.RECORDS + SEMI + SPACE + str(full_stats[self.SNP]) + NL)
            outfile.write(TAB + self.INDEL + SPACE + self.RECORDS + SEMI + SPACE + str(full_stats[self.INDEL]) + NL)
            outfile.write(
                TAB + self.BIALLELIC + SPACE + self.RECORDS + SEMI + SPACE + str(full_stats[self.BIALLELIC]) + NL)
            outfile.write(
                TAB + self.MULTIALLELIC + SPACE + self.RECORDS + SEMI + SPACE + str(full_stats[self.MULTIALLELIC]) + NL)

            outfile.write(NL + "TOTAL SNV NUCLEOTIDE CHANGES" + NL)
            for change in full_stats_nuc_changes.keys():
                outfile.write(TAB + change + SEMI + SPACE + str(full_stats_nuc_changes[change]) + NL)

            outfile.write(NL + "PER CHROMOSOME SUMMARY STATISTICS" + NL)

            for chrom in ordered_chroms:
                outfile.write(NL + TAB + chrom + SEMI + NL)
                outfile.write(TAB + TAB + self.TOTAL + SPACE + self.RECORDS + SEMI + SPACE +
                              str(per_chrom_stats[chrom][self.TOTAL]) + NL)
                outfile.write(TAB + TAB + self.SNP + SPACE + self.RECORDS + SEMI + SPACE +
                              str(per_chrom_stats[chrom][self.SNP]) + NL)
                outfile.write(TAB + TAB + self.INDEL + SPACE + self.RECORDS + SEMI + SPACE +
                              str(per_chrom_stats[chrom][self.INDEL]) + NL)
                outfile.write(TAB + TAB + self.BIALLELIC + SPACE + self.RECORDS + SEMI + SPACE +
                              str(per_chrom_stats[chrom][self.BIALLELIC]) + NL)
                outfile.write(TAB + TAB + self.MULTIALLELIC + SPACE + self.RECORDS + SEMI + SPACE +
                              str(per_chrom_stats[chrom][self.MULTIALLELIC]) + NL)

                outfile.write(NL + TAB + "{CHROM} SNV NUCLEOTIDE CHANGES".format(CHROM=chrom) + NL)
                for change in full_stats_nuc_changes.keys():
                    outfile.write(TAB + TAB + change + SEMI + SPACE + str(per_chrom_nuc_changes[chrom][change]) + NL)
