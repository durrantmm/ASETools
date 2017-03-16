import os
from os.path import basename

from Bio import SeqIO

from mod.misc.string_constants import *
from mod.run_python_step_super import RunPythonStepSuper


class RunGetReferenceBases(RunPythonStepSuper):

    def __init__(self, output_dir, input_tsv, input_reference_fasta, chrom_column=1,
                 pos_column=2, output_file=None, logger=None):

        name = 'GetReferenceBases'
        output_dir = output_dir

        input = input_tsv
        output = output_file

        log_name = 'get_reference_bases.json'
        logger = logger

        super().__init__(name, output_dir, input, output, log_name, logger)

        self.input_reference_fasta = input_reference_fasta
        self.chrom_column = chrom_column
        self.pos_column = pos_column
        self.index_adjust = -1


    def process(self):
        fasta_reader = self.read_fasta_file()
        chrom_seq = None

        with open(os.path.join(self.output_dir, self.output), w) as outfile:
            for chrom, pos in self.read_tsv_file():
                while not chrom_seq or chrom_seq.id != chrom:
                    chrom_seq = next(fasta_reader)

                reference_base = chrom_seq.seq[pos+self.index_adjust]
                outfile.write(TAB.join([chrom, str(pos), reference_base])+NL)


    def read_tsv_file(self):
        with open(self.input) as sites_in:
            for line in sites_in:
                line = line.split()
                chrom, pos = line[self.chrom_column+self.index_adjust], int(line[self.pos_column+self.index_adjust])
                yield chrom, pos


    def read_fasta_file(self):
        with open(self.input_reference_fasta, r) as infile:
            for record in SeqIO.parse(infile, fasta_str):
                yield record


    def handle_output(self, output_dir, output, input):
        if not output:
            output = input.split(DOT)[0]+DOT+self.name+DOT+tsv_str
        return basename(output)








