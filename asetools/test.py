import sys

from mod.misc.log import SimpleLog
from mod.pipeline.run.steps.star_align import RunStarAlign
from mod.pipeline.run.steps.add_read_groups import RunPicardAddReadGroups
from mod.pipeline.run.steps.mark_duplicates import RunPicardMarkDuplicates
from mod.pipeline.run.steps.split_n_cigar_reads import RunGATKSplitNCigarReads
from mod.pipeline.run.steps.rnaseq_base_recalibrator import RunGATKRNAseqBaseRecalibrator
from mod.pipeline.run.steps.print_reads import RunGATKPrintReads
from mod.pipeline.run.steps.haplotype_caller import RunGATKHaplotypeCaller
from mod.pipeline.run.steps.variant_filtration import RunGATKVariantFiltration


def test_star_align():
    log = SimpleLog()
    star_align = RunStarAlign(output_dir='tests/star_align_test1',
                              fastq1='examples/small.1.fq.gz',
                              fastq2='examples/small.2.fq.gz',
                              logger=log)
    star_align.run()
    print('Your output file of interest is at {PATH}'.format(PATH=star_align.retrieve_output_path()))


def test_add_read_groups():
    log = SimpleLog()
    add_read_groups1 = RunPicardAddReadGroups(output_dir='tests/add_read_groups_test1',
                                              input_sam='examples/smallAligned.out.sam',
                                              logger=log)
    add_read_groups1.run()
    print('Your output file of interest is at {PATH}'.format(PATH=add_read_groups1.retrieve_output_path()))

    add_read_groups2 = RunPicardAddReadGroups(output_dir='tests/add_read_groups_test2',
                                              input_sam='examples/smallAligned.out.sam',
                                              output_bam='specified_file.bam',
                                              logger=log)
    add_read_groups2.run()
    print('Your output file of interest is at {PATH}'.format(PATH=add_read_groups2.retrieve_output_path()))


def test_mark_duplicates():
    log = SimpleLog()

    mark_duplicates = RunPicardMarkDuplicates(output_dir='tests/mark_duplicates_test1',
                                               input_bam='examples/smallAligned.RG.bam',
                                               output_bam='examples/smallAligned.RG.MG.bam',
                                               logger=log)
    mark_duplicates.run()
    print('Your output file of interest is at {PATH}'.format(PATH=mark_duplicates.retrieve_output_path()))


def test_split_n_cigar_reads():
    log = SimpleLog()

    split_reads = RunGATKSplitNCigarReads(output_dir='tests/split_reads_test1',
                                          input_bam='examples/smallAligned.RG.MG.bam',
                                          output_bam='examples/smallAligned.RG.MG.SPLIT.bam',
                                          logger=log)

    split_reads.run()
    print('Your output file of interest is at {PATH}'.format(PATH=split_reads.retrieve_output_path()))


def test_base_recalibrator():
    log = SimpleLog()

    recal = RunGATKRNAseqBaseRecalibrator(output_dir='tests/base_recalibrator_test1',
                                                input_bam='examples/smallAligned.RG.MG.SPLIT.bam',
                                                logger=log)

    recal.run()
    print('Your output file of interest is at {PATH}'.format(PATH=recal.retrieve_output_path()))


def test_print_reads():
    log = SimpleLog()

    print_reads = RunGATKPrintReads(output_dir='tests/print_reads_test1',
                                                input_bam='examples/smallAligned.RG.MG.SPLIT.bam',
                                                input_recal_table="examples/recal.table",
                                                output_bam='smallAligned.RG.MG.SPLIT.RECAL.bam',
                                                logger=log)

    print_reads.run()
    print('Your output file of interest is at {PATH}'.format(PATH=print_reads.retrieve_output_path()))


def test_haplotype_caller():
    log = SimpgileLog()

    haplotype_caller = RunGATKHaplotypeCaller(output_dir='tests/haplotype_caller_test1',
                                                input_bam='examples/smallAligned.RG.MG.SPLIT.RECAL.bam',
                                                output_vcf='smallAligned.vcf',
                                                logger=log)

    haplotype_caller.run()
    print('Your output file of interest is at {PATH}'.format(PATH=haplotype_caller.retrieve_output_path()))

def test_variant_filtration():
    log = SimpleLog()

    variant_filtration = RunGATKVariantFiltration(output_dir='tests/variant_filtration_test1',
                                                input_vcf='examples/smallAligned.vcf',
                                                logger=log)

    variant_filtration.run()
    print('Your output file of interest is at {PATH}'.format(PATH=variant_filtration .retrieve_output_path()))


if __name__ == '__main__':

    which = sys.argv[1]

    if which == 'star_align' or which == 'all':
        test_star_align()

    if which == 'add_read_groups' or which == 'all':
        test_add_read_groups()

    if which == 'mark_duplicates' or which == 'all':
        test_mark_duplicates()

    if which == 'split_reads' or which == 'all':
        test_split_n_cigar_reads()

    if which == 'base_recal' or which == 'all':
        test_base_recalibrator()

    if which == 'print_reads' or which == 'all':
        test_print_reads()

    if which == 'haplotype_caller' or which == 'all':
        test_haplotype_caller()

    if which == 'variant_filter' or which == 'all':
        test_variant_filtration()


