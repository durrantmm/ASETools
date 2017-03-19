"""
AUTHOR: Matt Durrant

This module contains a RunProcessStepSuper subclass called RunFishersExactTest.

It iterates through each line of the input file and performs a Fisher’s exact test on the case/control read count data.
This test can determine if the difference in allele counts between cases and controls is significant or not.
This script also filters out any variant that variants with low coverage (< 10 reads) or that appear to be homozygous.
P-values are corrected for multiple testing using the Bonferroni correction, and then FDR q-values are calculated using
a downloaded package called qvalue (available at https://github.com/nfusi/qvalue).
"""

import os
import numpy as np
from mod.misc.string_constants import *
from mod.misc.integer_constants import *
from mod.process_step_superclass import RunProcessStepSuper
from scipy.stats import fisher_exact
from mod.misc import qvalue


class RunFishersExactTest(RunProcessStepSuper):
    """
    A class that that executes a Fisher's Exact Test on an input file or read counts.
    Also includes multiple testing correction.
    """

    def __init__(self, output_dir, read_count_data, filter_ratio_low=0.1, filter_ratio_high=0.9, min_count=10,
                 output_file=None, logger=None):
        """
        The constructor class for a RunFishersExactTest object.
        :param output_dir: The output directory.
        :param read_count_data: A path to read count data, as formatted by the protocol PrepareReadCountData.
        :param filter_ratio_low: The lower bound for the allele frequency ratio filter.
        :param filter_ratio_high: The upper bound for the allele frequency ratio filter.
        :param min_count: The minimum number of reads for cases and controls.
        :param output_file: The output file.
        :param logger: The logger to track progress.
        """

        name = 'FishersExactTest'
        output_dir = output_dir

        input_file = read_count_data
        output_file = output_file

        log_name = 'fishers_exact_test.json'
        logger = logger

        super().__init__(name, output_dir, input_file, output_file, log_name, logger)

        self.filter_ratio_low = filter_ratio_low
        self.filter_ratio_high = filter_ratio_high
        self.min_count = min_count

        # Keeps track of the strings to be used to specify different fields
        self.treatment_s, self.chrom_s, self.pos_s, self.ref_s, self.alt_s, self.case_alt_count_s, \
        self.case_ref_count_s, self.case_total_count_s, self.control_alt_count_s, self.control_ref_count_s, \
        self.control_total_count_s, self.oddsratio_s, self.pval_s, self.bonf_p_s, self.qval_s = \
            ['TREATMENT', 'CHROM', 'POS', 'REF', 'ALT', 'CASE_ALT_COUNT', 'CASE_REF_COUNT', 'CASE_TOTAL_COUNT',
             'CONTROL_ALT_COUNT', 'CONTROL_REF_COUNT', 'CONTROL_TOTAL_COUNT', 'OR', 'PVAL', 'BONF_PVAL', 'QVAL']

        # Keeps track of the strings used to specify input fields
        self.input_header = [self.treatment_s, self.chrom_s, self.pos_s, self.ref_s, self.alt_s, self.case_alt_count_s,
                             self.case_ref_count_s, self.case_total_count_s, self.control_alt_count_s,
                             self.control_ref_count_s, self.control_total_count_s]

        # Keeps track of the strings used to specify output fields
        self.output_header = [self.treatment_s, self.chrom_s, self.pos_s, self.ref_s, self.alt_s, self.case_alt_count_s,
                              self.case_ref_count_s, self.case_total_count_s, self.control_alt_count_s,
                              self.control_ref_count_s, self.control_total_count_s, self.oddsratio_s, self.pval_s,
                              self.bonf_p_s, self.qval_s]

    def process(self):
        """
        The primary process step for the class.
        """

        tested_snps = []
        for snp in self.parse_read_counts():

            # Checks to see if the snp fails the filters, skips it if it fails.
            if not self.passes_count_filter(snp) or not self.passes_ratio_filter(snp):
                continue

            # Creates a contingency table to be analyzed by the fishers exact test
            contingency_table = [[snp[self.case_ref_count_s], snp[self.control_ref_count_s]],
                                 [snp[self.case_alt_count_s], snp[self.control_alt_count_s]]]

            # Uses the fisher exact test as implemented by scipy.stats to get odds ratio and p-value
            oddsratio, pval = fisher_exact(contingency_table)
            snp[self.oddsratio_s] = oddsratio
            snp[self.pval_s] = pval
            tested_snps.append(snp)

        # Bonferonni correction is added
        results = self.bonferroni_correct(tested_snps)
        # q-value correction is added.
        results = self.qvalue_correct(results)

        # Writes the results fot a file
        with open(os.path.join(self.output_dir, self.output), w) as outfile:

            outfile.write(TAB.join(self.output_header) + NL)

            for line in results:
                outline = TAB.join([str(line[key]) for key in self.output_header])
                outfile.write(outline + NL)

    def bonferroni_correct(self, results):
        """
        Corrects the p-values of the results of the fisher exact test according to the bonferroni method.
        :param results: The results that have yet to be corrected by the bonferroni method
        :return: The same results, with an additional key: value pair for each test that includes the bonferroni
        corrected p-value.
        """

        # Calculates the bonferroni multiplier as the length of the results, or the total number of tests that
        # were performed.
        bonferroni_multiplier = len(results)

        # Iterates through all of the results and adds a new key: value pair indicating the bonferroni corrected p-value
        for result in results:
            # Adjusts the p-value by the bonferroni multiplier.
            bonf_p = (lambda x: BONF_MAX_PVAL if x > BONF_MAX_PVAL else x)(result[self.pval_s] * bonferroni_multiplier)

            # Adds the new bonferroni corrected p-value
            result[self.bonf_p_s] = bonf_p

        return results

    def qvalue_correct(self, results):
        """
        Calcualtes the qvalue of the results of the fisher exact test according to the FDR.
        :param results: The results that have yet to be corrected by the FDR qvalue
        :return: The same results, with an additional key: value pair for each test that includes the FDR qvalue.
        """
        pvals = np.asarray([result[self.pval_s] for result in results])

        # Uses the qvalue package, which was downloaded from the internet.
        qvals = qvalue.estimate(pvals)

        for index in range(len(results)):
            results[index][self.qval_s] = qvals[index]

        return results

    def passes_ratio_filter(self, snp):
        """
        Makes sure at that either the cases or the controls fails the alternate allele ratio test.
        :param snp: Input snp as read in by self.process()
        :return: boolean True or False, pass or fail
        """
        case_ratio = snp[self.case_alt_count_s] / float(snp[self.case_total_count_s])
        control_ratio = snp[self.control_alt_count_s] / float(snp[self.control_total_count_s])

        if self.filter_ratio_low <= case_ratio <= self.filter_ratio_high:
            return True
        elif self.filter_ratio_low <= control_ratio <= self.filter_ratio_high:
            return True
        else:
            return False

    def passes_count_filter(self, snp):
        """
        Checks to see if either cases or controls fails the minimum count filter. If either fails, the snp fails.
        :param snp: Input snp as read in by self.process()
        :return: boolean True or False, pass or fail
        """
        if snp[self.case_total_count_s] < self.min_count or snp[self.control_total_count_s] < self.min_count:
            return False
        else:
            return True

    def parse_read_counts(self, header=True):
        """
        A method to parse the read counts.
        :param header: The header of the file to be read in
        :return: yields a snp for each line in the file.
        """

        with open(self.input_file) as infile:
            if header:
                infile.readline()
            for line in infile:
                line = line.strip().split()
                snp = {self.input_header[i]: line[i] for i in range(len(self.input_header))}

                for key in snp.keys():
                    if snp[key].isdigit():
                        snp[key] = int(snp[key])

                yield snp
