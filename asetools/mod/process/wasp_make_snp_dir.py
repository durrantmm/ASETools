import gzip
from os.path import join

import vcf

from mod.misc.string_constants import *
from mod.run_process_step_super import RunProcessStepSuper


class RunMakeWaspSnpDir(RunProcessStepSuper):

    def __init__(self, output_dir, input_sorted_vcf, logger=None):

        name = 'MakeWaspSnpDir'
        output_dir = output_dir

        input = input_sorted_vcf
        output = output_dir

        log_name = 'make_wasp_snp_dir.json'
        logger = logger

        super().__init__(name, output_dir, input, output, log_name, logger)

        self.file_suffix = '.snps.txt.gz'

    def process(self):
        reader = vcf.Reader(filename=self.input)

        snp_files = {}
        for rec in reader:
            if rec.CHROM not in snp_files.keys():
                snp_files[rec.CHROM] = gzip.open(join(self.output_dir, rec.CHROM+self.file_suffix), 'wt')

            snp_files[rec.CHROM].write(SPACE.join(map(str, [rec.POS, rec.REF, rec.ALT[0]]))+NL)

        for chrom, out in snp_files.items():
            out.close()



    def save_log(self):
        pass

    def prep_chrom_snps(self, snps):
        return NL.join(map(lambda x: SPACE.join(map(str, x)), snps))







