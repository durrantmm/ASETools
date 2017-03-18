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

        super().__init__(name, output_dir, input, output, log_name, logger)

        self.add_chr = add_chr


    def process(self):
        print("YEP")