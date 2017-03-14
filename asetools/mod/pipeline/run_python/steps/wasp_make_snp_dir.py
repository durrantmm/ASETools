import vcf, os
from mod.misc.string_constants import *
from os.path import basename, join
from mod.pipeline.run_python.run_python_step_super import RunPythonStepSuper
from mod.misc.bash import gzip_file

class RunMakeWaspSnpDir(RunPythonStepSuper):

    def __init__(self, output_dir, input_sorted_vcf, logger=None):

        name = 'MakeWaspSnpDir'
        output_dir = output_dir

        input = input_sorted_vcf
        output = output_dir

        log_name = 'make_wasp_snp_dir.json'
        logger = logger

        super().__init__(name, output_dir, input, output, log_name, logger)

        self.vcf_file_suffix = '.vcf'
        self.file_suffix = '.snps.txt'
        self.gzip_suffix = '.gz'


    def process(self):
        reader = vcf.Reader(open(self.input))


        snp_files = {}
        for rec in reader:
            if rec.CHROM not in snp_files.keys():
                snp_files[rec.CHROM] = [join(self.output_dir, rec.CHROM+self.vcf_file_suffix),
                                        vcf.Writer(open(join(self.output_dir, rec.CHROM+self.vcf_file_suffix), 'w'), reader)]

            snp_files[rec.CHROM][1].write_record(rec)

        for chrom, value in snp_files.items():
            filename, out = value
            out.close()
            gzip_file(filename)





    def save_log(self):
        pass

    def prep_chrom_snps(self, snps):
        return NL.join(map(lambda x: SPACE.join(map(str, x)), snps))







