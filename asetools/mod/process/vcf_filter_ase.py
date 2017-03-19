"""
This module contains a RunProcessStepSuper subclass called RunVcfFilterASE.

This script takes a VCF file as input, and it keeps only variants that are biallelic, heterozygous single nucleotide
variants (SNVs). These scripts are used fro downstream ASE analysis. This script uses the PyVCF object-oriented module
to parse the VCF file.
"""

from os.path import join
import vcf
from mod.misc.string_constants import *
from mod.process_step_superclass import RunProcessStepSuper


class RunVcfFilterASE(RunProcessStepSuper):
    """
    This class takes a VCF file as input, and it keeps only variants that are biallelic, heterozygous single nucleotide
    variants (SNVs). These scripts are used fro downstream ASE analysis. This class uses the PyVCF object-oriented module
    to parse the VCF file.
    """

    def __init__(self, output_dir, input_vcf, output_vcf=None, min_one_het=True, hom_ref_hom_alt_is_het=True,
                 autosomal_only=True, biallelic_only=True, no_indels=True, logger=None):
        """
        This is the constructor for a RunVcfFilterASE object.
        :param output_dir: The output directory.
        :param input_vcf: The input VCF
        :param output_vcf: The output VCF
        :param min_one_het: Turns on the minimum one heterozygous variant filter.
        :param hom_ref_hom_alt_is_het: Turns on the homozygous reference and homozygous wildtype filter.
        :param autosomal_only: Filters to only autosomal chromosomes.
        :param biallelic_only: Filters to only biallelic variants
        :param no_indels: Filters out the indels.
        :param logger: Logger to track progress.
        """
        name = 'VCFFilterASE'
        output_dir = output_dir

        input_file = input_vcf
        output_file = output_vcf

        log_name = 'filter_vcf.json'
        logger = logger

        super().__init__(name, output_dir, input_file, output_file, log_name, logger, output_suffix='vcf')

        self.min_one_het = min_one_het
        self.hom_ref_hom_alt_is_het = hom_ref_hom_alt_is_het
        self.autosomal_only = autosomal_only
        self.biallelic_only = biallelic_only
        self.no_indels = no_indels

        self.autosomal_chroms = [chr1, chr2, chr3, chr4, chr5, chr6, chr7, chr8, chr9, chr10, chr11, chr12, chr13,
                                 chr14, chr15, chr16, chr17, chr18, chr19, chr20, chr21, chr22]

    def process(self):
        """
        Processes and filters the VCF
        """
        reader = vcf.Reader(filename=self.input_file)
        writer = vcf.Writer(open(join(self.output_dir, self.output), 'w'), reader)

        for rec in reader:
            # If the autosomal_only filter exists and it is NOT an autosomal chromosome, it skips the variant.
            if self.autosomal_only and rec.CHROM not in self.autosomal_chroms and \
                            rec.CHROM not in [c.strip('chr') for c in self.autosomal_chroms]:
                continue

            # If the self.biallelic_only filter is set and the record is not biallelic, it skips.
            elif self.biallelic_only and not self.is_biallelic(rec):
                continue

            # Skips if no indels is on and the record is an indel
            elif self.no_indels and rec.is_indel:
                continue

            # Writes the variant if min_one_het is on and it contains at least one het
            elif self.min_one_het and self.contains_min_one_het(rec):
                writer.write_record(rec)
                continue

            # Writes the ariant if hom_ref_hom_alt_is_het is on and it passes the filter
            elif self.hom_ref_hom_alt_is_het and self.contains_both_homs(rec):
                writer.write_record(rec)
                continue

            # If it gets through all the filters, write the variant to a file.
            else:
                writer.write_record(rec)

    def is_biallelic(self, record):
        if len(record.ALT) == 1:
            return True
        else:
            return False

    def contains_min_one_het(self, record):
        if len(record.get_hets()) >= 1:
            return True
        else:
            return False

    def contains_both_homs(self, record):
        if len(record.get_hom_refs()) >= 1 and len(record.get_hom_alts()) >= 1:
            return True
        else:
            return False
