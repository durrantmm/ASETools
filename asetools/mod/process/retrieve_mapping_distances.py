import sys
import pysam, vcf
import os
from mod.misc.string_constants import *

from mod.run_process_step_superclass import RunProcessStepSuper


class RunRetrieveMappingDistances(RunProcessStepSuper):

    def __init__(self, output_dir, input_bam, input_vcf, output_file=None, logger=None):

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
        position = position + self.bam_index_correction
        ref_read_distances = []
        alt_read_distances = []

        for pileupcolumn in bamfile.pileup(chrom, position, position+1, truncate=True):

            for pileupread in pileupcolumn.pileups:

                if not pileupread.is_del and not pileupread.is_refskip:

                    read1 = pileupread.alignment
                    allele = read1.query_sequence[pileupread.query_position]
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

        if read1.is_unmapped or read2.is_unmapped:
            return None
        else:
            reference_positions = [read1.reference_start, read1.reference_end-1,
                                   read2.reference_start, read2.reference_end-1]
            distance = max(reference_positions) - min(reference_positions)
            return distance


    def complementary_base(self, base):
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