"""
This module contains a RunProcessStepSuper subclass called RunRetrieveMappingDistances.

This script takes a VCF of differential ASE candidate variants as one input, and a BAM file of aligned RNAseq data as a
second input. It then retrieves all reads from the BAM file that overlap a variant locus, and determines the mapping
distance between the two paired reads. One can then compare the mapping distance distributions of the reference and the
alternate allele visually by plotting them. If the alleles differ drastically in their read mapping distance
distributions, it is an indication that allele-specific splicing may be confounding the analysis.
"""

import pysam, vcf
import os
from mod.misc.string_constants import *

from mod.process_step_superclass import RunProcessStepSuper


class RunRetrieveMappingDistances(RunProcessStepSuper):

    def __init__(self, output_dir, input_bam, input_vcf, output_file=None, logger=None):
        """
        This is the constructor for a RunRetrieveMappingDistances object.
        :param output_dir: The output directory.
        :param input_bam: The input BAM.
        :param input_vcf: The input VCF.
        :param output_file:  The output file.
        :param logger: The logger for tracking progress.
        """

        name = 'RetrieveMappingDistances'
        output_dir = output_dir

        input = input_bam
        output = output_file

        log_name = 'retrieve_mapping_distances.json'
        logger = logger

        super().__init__(name, output_dir, input, output, log_name, logger)

        self.input_vcf = input_vcf
        self.bam_index_correction = -1
        self.ref_s = 'REF'
        self.alt_s = 'ALT'

        self.out_header = TAB.join(['CHROM', 'POS', 'REF', 'ALT', 'ALLELE', 'MAPPING_DISTANCE'])


    def process(self):
        """
        This runs the main process script to retrieve all of the mapping distances for ll reads that overlap with
        variants in the VCF file
        """
        bam_reader = pysam.AlignmentFile(self.input, "rb")
        vcf_reader = vcf.Reader(filename=self.input_vcf)

        with open(os.path.join(self.output_dir, self.output), w) as outfile:

            outfile.write(self.out_header+NL)

            for snp in vcf_reader:
                chrom, pos, ref, alt = snp.CHROM, snp.POS, snp.REF, snp.ALT[0]
                ref_distances, alt_distances = self.retrieve_mapping_distances(chrom, pos, ref, alt, bam_reader)

                for dist in ref_distances:
                    outline = TAB.join(map(str, [chrom, pos, ref, alt, self.ref_s, dist]))
                    outfile.write(outline+NL)

                for dist in alt_distances:
                    outline = TAB.join(map(str, [chrom, pos, ref, alt, self.alt_s, dist]))
                    outfile.write(outline+NL)


    def retrieve_mapping_distances(self, chrom, position, ref, alt, bamfile):
        """
        Parses through the bam file to retrieve all of the referencae and alternate allele read pair mapping distances
        that overlap the given position
        :param chrom: The variant chromosome.
        :param position: The variant position.
        :param ref: The referance allele.
        :param alt: The alternate allele.
        :param bamfile: The indexed bam file.
        :return:
        """
        position = position + self.bam_index_correction
        ref_read_distances = []
        alt_read_distances = []

        # Gets the pileup columns covering the read.
        for pileupcolumn in bamfile.pileup(chrom, position, position+1, truncate=True):

            # Gets each of the reads in each pileup column.
            for pileupread in pileupcolumn.pileups:

                # Makes sure the read meets some important filters.
                if not pileupread.is_del and not pileupread.is_refskip:

                    read1 = pileupread.alignment
                    allele = read1.query_sequence[pileupread.query_position]

                    # Gets the raad mate pair if it exists.
                    try:
                        read2 = bamfile.mate(read1)
                    except ValueError:
                        continue

                    distance = self.calc_mapping_distance(read1, read2)

                    if distance:
                        if allele == ref:
                            ref_read_distances.append(distance)
                        elif allele == alt:
                            alt_read_distances.append(distance)

        return sorted(ref_read_distances), sorted(alt_read_distances)


    def calc_mapping_distance(self, read1, read2):
        """
        Calculates the read distance between two paired reads
        """
        if read1.is_unmapped or read2.is_unmapped:
            return None
        else:
            reference_positions = [read1.reference_start, read1.reference_end-1,
                                   read2.reference_start, read2.reference_end-1]
            distance = max(reference_positions) - min(reference_positions)
            return distance


    def complementary_base(self, base):
        """
        Gets a complementary base for the given input base.
        """
        if base == 'A':
            return 'T'
        elif base == 'T':
            return 'A'
        elif base == 'G':
            return 'C'
        elif base == 'C':
            return 'G'
        else:
            return base