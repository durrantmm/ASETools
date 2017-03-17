import os
from os.path import basename

from Bio import SeqIO

from mod.misc.string_constants import *
from mod.run_python_step_super import RunPythonStepSuper


class RunPrepareReadCountData(RunPythonStepSuper):

    def __init__(self, output_dir, file_paths, output_file=None, logger=None):

        name = 'PrepareReadCountData'
        output_dir = output_dir

        input = file_paths
        output = output_file

        log_name = 'prepare_read_count_data.json'
        logger = logger

        super().__init__(name, output_dir, input, output, log_name, logger)


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







