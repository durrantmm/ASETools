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

        self.autosomal_chroms = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9'
                                 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17',
                                 'chr18', 'chr19', 'chr20', 'chr21', 'chr22']


    def process(self):
        reader = vcf.Reader(open(self.input),)
        writer = vcf.Writer(open(self.output, 'w'), reader)

        for rec in reader:

            if self.autosomal_only and rec.CHROM not in self.autosomal_chroms or \
                            rec.CHROM not in [c.strip('chr') for c in self.autosomal_chroms]:
                continue

            if self.biallelic_only and not self.is_biallelic(rec):
                continue

            print(rec)



    def is_biallelic(self, record):
        True









