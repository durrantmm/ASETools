import vcf
import os
from os.path import basename, join
from mod.misc.string_constants import *
from mod.pipeline.run_python.run_python_step_super import RunPythonStepSuper
from Bio import SeqIO
from glob import glob
import gzip



class RunGetReferenceBases(RunPythonStepSuper):

    def __init__(self, output_dir, input_tsv, input_reference_fasta, chrom_column=1,
                 pos_column=2, output_file=None, logger=None):

        name = 'GetReferenceBases'
        output_dir = output_dir

        input = input_tsv
        output = output_file

        log_name = 'gene_annotate_sites.json'
        logger = logger

        super().__init__(name, output_dir, input, output, log_name, logger)

        self.input_reference_fasta = input_reference_fasta
        self.chrom_column = chrom_column
        self.pos_column = pos_column
        self.index_adjust = -1

        self.autosomal_chroms = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9'
                                 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17',
                                 'chr18', 'chr19', 'chr20', 'chr21', 'chr22']

    def process(self):
        fasta_reader = self.read_fasta_file()
        current_chrom = None
        chrom_seq = None

        for chrom, pos in self.read_tsv_file():
            if chrom != current_chrom:
                chrom_seq = next(fasta_reader)

            print(chrom_seq.id)


    def read_tsv_file(self):
        with open(self.input) as sites_in:
            for line in sites_in:
                line = line.split()
                chrom, pos = line[self.chrom_column+self.index_adjust], line[self.pos_column+self.index_adjust]
                yield chrom, pos


    def read_fasta_file(self):
        with open(self.input_reference_fasta, 'r') as infile:
            for record in SeqIO.parse(infile, 'fasta'):
                yield record


    def handle_output(self, output_dir, output, input):
        if not output:
            output = input.split(DOT)[0]+DOT+self.name+DOT+'tsv'
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








