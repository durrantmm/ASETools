"""
AUTHOR: Matt Durrant

This module contains a RunProcessStepSuper subclass called RunPrepareReadCountData.

This script takes the output of the pipeline implemented as Pipeline-ASEReadCounterWASP, which produces TSV files that
contain allele counts for the heterozygous variant sites of interest. The data set I analyzed has ten samples in total,
but many of them are replicates of the same time point. PrepareReadCountData merges the replicates by summing their
read counts. Since each of the three time points (9 hours, 18 hours, 24 hours) has both cases and controls, the read
count data from both cases and controls are organized so that they appear on the same line in the output.
"""

import os
from mod.misc.string_constants import *
from mod.process_step_superclass import RunProcessStepSuper
from collections import defaultdict
from operator import itemgetter


class RunPrepareReadCountData(RunProcessStepSuper):
    def __init__(self, output_dir, cases_paths, controls_paths, output_file=None, logger=None):
        """
        The constructor class for a RunPrepareReadCountData object.
        :param output_dir: The output directory.
        :param cases_paths: The list of paths to the read count files for the cases.
        :param controls_paths: The list of paths to the read count files for the controls.
        :param output_file: The path to the output file.
        :param logger: The logger for tracking process.
        """
        name = 'PrepareReadCountData'
        output_dir = output_dir

        input_file = cases_paths[0][0]
        output_file = output_file

        log_name = 'prepare_read_count_data.json'
        logger = logger

        super().__init__(name, output_dir, input_file, output_file, log_name, logger)

        self.cases = cases_paths
        self.controls = controls_paths

        # A list of the ordered human chromsoomes to ensure that output reads are in the correct format.
        self.ordered_chroms = [chrM, chr1, chr2, chr3, chr4, chr5, chr6, chr7, chr8, chr9, chr10, chr11, chr12, chr13,
                               chr14, chr15, chr16, chr17, chr18, chr19, chr20, chr21, chr22, chrX, chrY]

        # The output header
        self.header = TAB.join(['TREATMENT', 'CHROM', 'POS', 'REF', 'ALT', 'CASE_ALT_COUNT', 'CASE_REF_COUNT',
                                'CASE_TOTAL_COUNT', 'CONTROL_ALT_COUNT', 'CONTROL_REF_COUNT', 'CONTROL_TOTAL_COUNT'])

        # The treatment string to label each new line by treatment.
        self.treatment_str = 'treatment{NUM}'

    def process(self):
        """
        The primary process step for the class.
        """

        merged_cases = []
        for treatment in self.cases:
            # Merges the read counts data that share the same treatment
            merged_cases.append(self.merge_read_counts(treatment))

        merged_controls = []
        for treatment in self.controls:
            # Merges the read counts data that share the same treatment
            merged_controls.append(self.merge_read_counts(treatment))

        # Formats the results correctly.
        final_output = self.format_final_output(merged_cases, merged_controls)

        # Writes the results to the output file.
        with open(os.path.join(self.output_dir, self.output), w) as outfile:

            outfile.write(self.header + NL)

            for line in final_output:
                outfile.write(TAB.join(map(str, line)) + NL)

    def merge_read_counts(self, read_count_paths):
        """
        Merges replicates of the same treatment.
        :param read_count_paths: The paths to the read count files to merge
        :return: A dictionary of the merged read count data.
        """
        count_dict = defaultdict(lambda: defaultdict(list))

        for path in read_count_paths:
            reader = self.read_count_reader(path)

            for chrom, pos, ref, alt, refCount, altCount, totalCount in reader:
                # Stores the reference allele count, alternate allele count, and total allele count
                dict_key = (chrom, pos, ref, alt)

                if dict_key in count_dict[chrom]:
                    count_dict[chrom][dict_key][0] += refCount
                    count_dict[chrom][dict_key][1] += altCount
                    count_dict[chrom][dict_key][2] += totalCount

                else:
                    count_dict[chrom][dict_key] = [refCount, altCount, totalCount]

        return dict(count_dict)

    def format_final_output(self, merged_cases, merged_controls):
        """
        Formats the output data so that it can be properly analyzed by the FishersExactTest protocol.
        :param merged_cases: The merged cases as produced by self.merge_read_counts()
        :param merged_controls: The merged controls as produced by self.merge_read_counts()
        :return:  The correctly formatted final output.
        """

        final_output = []

        for index, case_counts in enumerate(merged_cases):

            control_counts = merged_controls[index]

            # iterates through all of the chromosomes so that the output has the correct chromosome order.
            for chrom in self.ordered_chroms:

                # Checks that the chromosome is in either the cases or the controls.
                if chrom in case_counts.keys() and chrom in control_counts.keys():

                    # Uses sets to get a list of unique variant positions
                    all_chrom_keys = list(set(case_counts[chrom].keys()) | set(control_counts[chrom].keys()))
                    # Converts back into a list and sorts by position.
                    all_chrom_keys.sort(key=itemgetter(1))

                    for key in all_chrom_keys:

                        # If variant is missing from cases, sets all counts to 0
                        if key not in case_counts[chrom]:
                            case_counts[chrom][key] = [0, 0, 0]

                        # If variant is missing from controls, sets all counts to 0
                        elif key not in control_counts[chrom]:
                            control_counts[chrom][key] = [0, 0, 0]

                        # Retrieves the allele counts
                        chrom, pos, ref, alt = key
                        case_alt_count, case_ref_count, case_total_count = case_counts[chrom][key]
                        control_alt_count, control_ref_count, control_total_count = control_counts[chrom][key]

                        new_line = [self.treatment_str.format(NUM=index), chrom, pos, ref, alt,
                                    case_alt_count, case_ref_count, case_total_count,
                                    control_alt_count, control_ref_count, control_total_count]

                        final_output.append(new_line)

                elif chrom not in case_counts.keys() and chrom not in control_counts.keys():
                    continue

                # Handles an error edge case
                else:
                    print("Error: not the same number of chromosomes in each read count file.")

        return final_output

    def read_count_reader(self, path, header=True):
        """
        Produces a generator that parses the read count files.
        """
        with open(path) as infile:

            if header:
                infile.readline()

            for line in infile:
                line = line.strip().split()
                chrom, position, ident, refAllele, altAllele, refCount, altCount, totalCount = line[:8]
                yield chrom, int(position), refAllele, altAllele, int(refCount), int(altCount), int(totalCount)
