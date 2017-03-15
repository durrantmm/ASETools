import vcf
from os.path import basename, join
from mod.pipeline.run_python.run_python_step_super import RunPythonStepSuper

class RunFilterVCF(RunPythonStepSuper):

    def __init__(self, output_dir, input_vcf, output_vcf, min_one_het=True, hom_ref_hom_alt_is_het=True,
                 autosomal_only=True, biallelic_only=True, no_indels=True, logger=None):

        name = 'FilterVCF'
        output_dir = output_dir

        input = input_vcf
        output = self.hand

        log_name = 'filter_vcf.json'
        logger = logger

        super().__init__(name, output_dir, input, output, log_name, logger)

        self.min_one_het = min_one_het
        self.hom_ref_hom_alt_is_het = hom_ref_hom_alt_is_het
        self.autosomal_only = autosomal_only
        self.biallelic_only = biallelic_only
        self.no_indels = no_indels

        self.autosomal_chroms = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9'
                                 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17',
                                 'chr18', 'chr19', 'chr20', 'chr21', 'chr22']

    def process(self):
        reader = vcf.Reader(open(self.input))
        writer = vcf.Writer(open(join(self.output_dir, self.output), 'w'), reader)
        print(join(self.output_dir, self.output))

        for rec in reader:
            print(rec)

            if self.autosomal_only and rec.CHROM not in self.autosomal_chroms and \
                            rec.CHROM not in [c.strip('chr') for c in self.autosomal_chroms]:
                continue

            elif self.biallelic_only and not self.is_biallelic(rec):
                continue

            elif self.no_indels and rec.is_indel:
                continue

            elif self.min_one_het and not self.contains_min_one_het(rec):
                continue

            elif self.hom_ref_hom_alt_is_het and not self.contains_both_homs(rec):
                continue

            else:
                writer.write_record(rec)


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
        if len(record.get_hom_refs) >= 1 and len(record.get_hom_alts) >= 1:
            return True
        else:
            return False








