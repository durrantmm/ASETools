import os, sys

from mod.misc.string_constants import *
from mod.run_process_step_super import RunProcessStepSuper
from collections import defaultdict
from operator import itemgetter


class RunPrepareReadCountData(RunProcessStepSuper):

    def __init__(self, output_dir, cases_paths, controls_paths, output_file=None, logger=None):

        name = 'PrepareReadCountData'
        output_dir = output_dir

        input = [cases_paths, controls_paths]
        output = output_file

        log_name = 'prepare_read_count_data.json'
        logger = logger

        super().__init__(name, output_dir, input, output, log_name, logger)
        self.cases = cases_paths
        self.controls = controls_paths
        self.ordered_chroms = [chrM, chr1, chr2, chr3, chr4, chr5, chr6, chr7, chr8, chr9, chr10, chr11, chr12, chr13,
                               chr14, chr15, chr16, chr17, chr18, chr19, chr20, chr21, chr22, chrX, chrY]
        self.header = TAB.join(['TREATMENT', 'CHROM', 'POS', 'REF', 'ALT', 'CASE_ALT_COUNT', 'CASE_REF_COUNT',
                                'CASE_TOTAL_COUNT', 'CONTROL_ALT_COUNT', 'CONTROL_REF_COUNT', 'CONTROL_TOTAL_COUNT'])
        self.treatment_str = 'treatment{NUM}'


    def process(self):
        merged_cases = []
        for treatment in self.cases:
            merged_cases.append(self.merge_read_counts(treatment))

        merged_controls = []
        for treatment in self.controls:
            merged_controls.append(self.merge_read_counts(treatment))


        final_output = self.format_final_output(merged_cases, merged_controls)

        with open(os.path.join(self.output_dir, self.output), w) as outfile:
            outfile.write(self.header+NL)
            for line in final_output:
                outfile.write(TAB.join(map(str, line))+NL)


    def merge_read_counts(self, read_count_paths):
        count_dict = defaultdict(lambda: defaultdict(list))

        for path in read_count_paths:
            reader = self.read_count_reader(path)
            for chrom, pos, ref, alt, refCount, altCount, totalCount in reader:
                dict_key = (chrom, pos, ref, alt)
                if dict_key in count_dict[chrom]:
                    count_dict[chrom][dict_key][0] += refCount
                    count_dict[chrom][dict_key][1] += altCount
                    count_dict[chrom][dict_key][2] += totalCount
                else:
                    count_dict[chrom][dict_key] = [refCount, altCount, totalCount]
        return dict(count_dict)


    def format_final_output(self, merged_cases, merged_controls):
        final_output = []

        for index, case_counts in enumerate(merged_cases):

            control_counts = merged_controls[index]

            for chrom in self.ordered_chroms:

                if chrom in case_counts.keys() and chrom in control_counts.keys():

                    all_chrom_keys = list(set(case_counts[chrom].keys()) | set(control_counts[chrom].keys()))
                    all_chrom_keys.sort(key=itemgetter(1))

                    for key in all_chrom_keys:

                        if key not in case_counts[chrom]:
                            case_counts[chrom][key] = [0, 0, 0]

                        elif key not in control_counts[chrom]:
                            control_counts[chrom][key] = [0, 0, 0]

                        chrom, pos, ref, alt = key
                        caseAltCount, caseRefCount, caseTotalCount = case_counts[chrom][key]
                        controlAltCount, controlRefCount, controlTotalCount = control_counts[chrom][key]

                        new_line = [self.treatment_str.format(NUM=index), chrom, pos, ref, alt,
                                    caseAltCount, caseRefCount, caseTotalCount,
                                    controlAltCount, controlRefCount, controlTotalCount]
                        final_output.append(new_line)

                elif chrom not in case_counts.keys() and chrom not in control_counts.keys():
                    continue

                else:
                    print("Error: not the same number of chromosomes in each read count file.")

        return final_output

    def read_count_reader(self, path, header=True):
        with open(path) as infile:

            if header:
                infile.readline()

            for line in infile:
                line = line.strip().split()
                chrom, position, id, refAllele, altAllele, refCount, altCount, totalCount = line[:8]
                yield chrom, int(position), refAllele, altAllele, int(refCount), int(altCount), int(totalCount)




    def handle_output(self, output_dir, output, input_file, suffix='tsv'):
        if not output or os.path.realpath(output) == os.path.realpath(input_file):
            output = self.name+DOT+suffix

        return os.path.basename(output)





