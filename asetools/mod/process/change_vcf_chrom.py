import re
import os
from mod.misc.string_constants import *

from mod.run_process_step_super import RunProcessStepSuper


class RunChangeVcfChrom(RunProcessStepSuper):

    def __init__(self, output_dir, input_vcf, add_chr=True, output_file=None, logger=None):

        name = 'ChangeVcfChrom'
        output_dir = output_dir

        input = input_vcf
        output = output_file

        log_name = 'change_vcf_chrom.json'
        logger = logger

        super().__init__(name, output_dir, input, output, log_name, logger, output_suffix='vcf')

        self.add_chr = add_chr
        self.chr_s = 'chr'


    def process(self):
        with open(self.input) as vcf_in:
            if self.add_chr:
                self.add_chr_parse_vcf(vcf_in)
            else:
                self.remove_chr_parse_vcf(vcf_in)


    def add_chr_parse_vcf(self, vcf_stream):
        with open(os.path.join(self.output_dir, self.output), w) as outfile:
            for line in vcf_stream:
                if re.search(r'contig=<', line):
                    line = re.sub(r'(?<=ID=)(?!{CHR_STRING})([^,>]+)'.format(CHR_STRING=self.chr_s),
                                  r'{CHR_STRING}\1'.format(CHR_STRING=self.chr_s), line)

                line = re.sub(r'^(?!{CHR_STRING})(\w+)'.format(CHR_STRING=self.chr_s),
                              r'{CHR_STRING}\1'.format(CHR_STRING=self.chr_s), line)
                outfile.write(line)


    def remove_chr_parse_vcf(self, vcf_stream):
        with open(os.path.join(self.output_dir, self.output), w) as outfile:
            for line in vcf_stream:
                if re.search(r'contig=<', line):
                    line = re.sub(r'(?<=ID=){CHR_STRING}'.format(CHR_STRING=self.chr_s), '', line)
                line = re.sub(r'^{CHR_STRING}'.format(CHR_STRING=self.chr_s), '', line)
                outfile.write(line)