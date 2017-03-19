"""
This module contains a RunProcessStepSuper subclass called RunChangeVcfChrom.

I developed this script to help me correct a common problem that I often came across:
different chromosome identifiers in different VCF files.

This script uses regular expressions to parse through a VCF file and replace all chromosome IDs that are labeled
as ‘1’ with ‘chr1’, or the opposite operation. Automating this conversion will save me a lot of time.
"""

import re
import os
from mod.misc.string_constants import *
from mod.process_step_superclass import RunProcessStepSuper


class RunChangeVcfChrom(RunProcessStepSuper):
    """
    This class runs the ChangeVcfChrom protocol
    """

    def __init__(self, output_dir, input_vcf, add_chr=True, output_file=None, logger=None):
        """
        The constructor for a RunChangeVcfChrom object.
        :param output_dir: The output directory.
        :param input_vcf: The input VCF file to be altered.
        :param add_chr: Whether or not to add (or remove when False) 'chr' from the VCF
        :param output_file: The name of the output file.
        :param logger: The logger to track progress.
        """
        name = 'ChangeVcfChrom'
        output_dir = output_dir

        input_file = input_vcf
        output_file = output_file

        log_name = 'change_vcf_chrom.json'
        logger = logger

        super().__init__(name, output_dir, input_file, output_file, log_name, logger, output_suffix='vcf')

        self.add_chr = add_chr
        self.chr_s = 'chr'

    def process(self):
        """
        Processes the input vcf, changes the chromosome identifiers using regular expressions, and then saves
        the output.
        """
        with open(self.input_file) as vcf_in:

            # Checks if it should add 'chr' from chromosomes
            if self.add_chr:
                self.add_chr_parse_vcf(vcf_in)
            # Otherwise it removes 'chr' from the contigs.
            else:
                self.remove_chr_parse_vcf(vcf_in)

    def add_chr_parse_vcf(self, vcf_stream):
        """
        This function adds the 'chr' chromosome prefix to the VCF file where appropriate.
        :param vcf_stream: A VCF file opened as a plain IO stream.
        """

        with open(os.path.join(self.output_dir, self.output), w) as outfile:

            for line in vcf_stream:

                # Adds 'chr' where the regular expression finds a contig match in the header lines
                # Ignores if 'chr' is already the prefix.
                if re.search(r'contig=<', line):
                    line = re.sub(r'(?<=ID=)(?!{CHR_STRING})([^,>]+)'.format(CHR_STRING=self.chr_s),
                                  r'{CHR_STRING}\1'.format(CHR_STRING=self.chr_s), line)

                # Adds 'chr' to all of the non-header lines
                # Ignores if 'chr' is already the prefix.
                line = re.sub(r'^(?!{CHR_STRING})(\w+)'.format(CHR_STRING=self.chr_s),
                              r'{CHR_STRING}\1'.format(CHR_STRING=self.chr_s), line)
                outfile.write(line)

    def remove_chr_parse_vcf(self, vcf_stream):
        """
        This function removes the 'chr' chromosome prefix from the VCF file where appropriate.
        :param vcf_stream: A VCF file opened as a plain IO stream.
        """

        with open(os.path.join(self.output_dir, self.output), w) as outfile:

            for line in vcf_stream:

                # Removes 'chr' where the regular expression finds a contig match in the header lines
                if re.search(r'contig=<', line):
                    line = re.sub(r'(?<=ID=){CHR_STRING}'.format(CHR_STRING=self.chr_s), '', line)

                # Removes 'chr' from all of the non-header lines
                line = re.sub(r'^{CHR_STRING}'.format(CHR_STRING=self.chr_s), '', line)
                outfile.write(line)
