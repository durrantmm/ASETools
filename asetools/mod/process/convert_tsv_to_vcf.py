from os.path import basename, join

import vcf

from mod.misc.string_constants import *
from mod.run_process_step_super import RunProcessStepSuper


class RunConvertTSVtoVCF(RunProcessStepSuper):

    def __init__(self, output_dir, input_tsv, chrom_column=1, pos_column=2, ref_column=3, alt_column=4,
                 gt_column=5, output_vcf=None, logger=None):

        name = 'ConvertTSVtoVCF'
        output_dir = output_dir

        input = input_tsv
        output = output_vcf

        log_name = 'filter_vcf.json'
        logger = logger

        super().__init__(name, output_dir, input, output, log_name, logger)

        self.chrom_column = chrom_column
        self.pos_column = pos_column
        self.ref_column = ref_column
        self.alt_column = alt_column
        self.gt_column= gt_column

        self.autosomal_chroms = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9'
                                 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17',
                                 'chr18', 'chr19', 'chr20', 'chr21', 'chr22']

    def process(self):
        reader = vcf.Reader(filename=self.input)
        writer = vcf.Writer(open(join(self.output_dir, self.output), 'w'), reader)

        for rec in reader:

            if self.autosomal_only and rec.CHROM not in self.autosomal_chroms and \
                            rec.CHROM not in [c.strip('chr') for c in self.autosomal_chroms]:
                continue

            elif self.biallelic_only and not self.is_biallelic(rec):
                continue

            elif self.no_indels and rec.is_indel:
                continue

            elif self.min_one_het and self.contains_min_one_het(rec):
                writer.write_record(rec)

            elif self.hom_ref_hom_alt_is_het and self.contains_both_homs(rec):
                writer.write_record(rec)

            else:
                continue


    def handle_output(self, output_dir, output, input):
        if not output:
            output = input.split(DOT)[0]+DOT+self.name+DOT+'vcf'
        return basename(output)

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








