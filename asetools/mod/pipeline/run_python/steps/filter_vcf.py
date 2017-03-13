import vcf
from mod.pipeline.run_python.run_python_step_super import RunPythonStepSuper

class RunFilterVCF(RunPythonStepSuper):

    def __init__(self, output_dir, input_vcf, output_vcf, min_one_het=True, autosomal_only=True, biallelic_only=True,
                 no_indels=True, logger=None):

        name = 'FilterVCF'
        output_dir = output_dir

        input = input_vcf
        output = output_vcf

        log_name = 'filter_vcf.json'
        logger = logger

        super().__init__(name, output_dir, input, output, log_name, logger)

        self.min_one_het = min_one_het
        self.autosomal_only = autosomal_only
        self.biallelic_only = biallelic_only
        self.no_indels = no_indels


    def process(self):
        reader = vcf.Reader(open(self.input),)
        writer = vcf.Writer(open(self.output, 'w'), reader)

        for line in reader:
            print(line)





