import sys

from mod.misc.log import SimpleLog
from mod.pipeline.run_process.steps.star_align import RunStarAlign
from mod.pipeline.run_process.steps.add_read_groups import RunPicardAddReadGroups
from mod.pipeline.run_process.steps.mark_duplicates import RunPicardMarkDuplicates
from mod.pipeline.run_process.steps.split_n_cigar_reads import RunGATKSplitNCigarReads
from mod.pipeline.run_process.steps.rnaseq_base_recalibrator import RunGATKRNAseqBaseRecalibrator
from mod.pipeline.run_process.steps.print_reads import RunGATKPrintReads
from mod.pipeline.run_process.steps.haplotype_caller import RunGATKHaplotypeCaller
from mod.pipeline.run_process.steps.variant_filtration import RunGATKVariantFiltration
from mod.pipeline.run_process.piped.rnaseq_variant_calling import RunRNASeqVariantCalling
from mod.pipeline.run_python.steps.vcf_filter_ase import RunVCFFilterASE
from mod.pipeline.run_python.steps.wasp_make_snp_dir import RunMakeWaspSnpDir
from mod.pipeline.run_process.steps.wasp_find_intersecting_snps import RunWaspFindIntersectingSnps
from mod.pipeline.run_process.steps.wasp_filter_remapped_reads import RunWaspFilterRemappedReads
from mod.pipeline.run_process.steps.samtools import RunSamtools
from mod.pipeline.run_process.steps.samtools_merge import RunSamtoolsMerge
from mod.pipeline.run_process.steps.samtools_sort import RunSamtoolsSort
from mod.pipeline.run_process.steps.samtools_index import RunSamtoolsIndex
from mod.pipeline.run_process.steps.ase_read_counter import RunGATKASEReadCounter


#
#   These are test cases that I've written to quickly check individual parts of the code.
#


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
    log = SimpleLog()

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

def test_rnaseq_variant_calling_pipe():
    log = SimpleLog()

    var_caller = RunRNASeqVariantCalling(output_dir="tests/VARIANT_CALLER",
                                         fastq1='examples/small.1.fq.gz',
                                         fastq2='examples/small.2.fq.gz',
                                         logger=log)

    var_caller.run()

def test_filter_vcf():
    log = SimpleLog()

    vcf_filter =  RunVCFFilterASE(output_dir="tests/filter_vcf",
                                  input_vcf="examples/smallAligned.FILTERED.vcf",
                                  output_vcf="smallAligned.FILTERED.HET.vcf",
                                  logger=log)
    vcf_filter.run()

def test_make_wasp_snp_dir():
    log = SimpleLog()

    make_snp_dir = RunMakeWaspSnpDir(output_dir="tests/make_wasp_snp_dir",
                                     input_sorted_vcf="examples/smallAligned.FILTERED.HET.vcf",
                                     logger=log)
    make_snp_dir.run()

def test_find_intersecting_snps():
    log = SimpleLog()

    inter_snps = RunWaspFindIntersectingSnps(output_dir="tests/wasp_find_intersecting_snps",
                                             input_bam="examples/smallAligned.RG.MG.bam",
                                             input_snp_dir="examples/make_wasp_snp_dir",
                                             logger=log)
    inter_snps.run()
    print('Your output file of interest is at {PATH}'.format(PATH=inter_snps.retrieve_output_path()))


def test_star_remap():
    log = SimpleLog()
    star_remap = RunStarAlign(output_dir='tests/star_remap',
                              fastq1='examples/smallAligned.RG.MG.remap.fq1.gz',
                              fastq2='examples/smallAligned.RG.MG.remap.fq2.gz',
                              logger=log)
    star_remap.run()
    print('Your output file of interest is at {PATH}'.format(PATH=star_remap.retrieve_output_path()))

def test_prep_star_remap():
    log = SimpleLog()
    add_read_groups1 = RunPicardAddReadGroups(output_dir='tests/prep_star_remap',
                                              input_sam='examples/smallAligned.remapped.sam',
                                              logger=log)
    add_read_groups1.run()
    out_bam = add_read_groups1.retrieve_output_path()

    mark_duplicates = RunPicardMarkDuplicates(output_dir='tests/prep_star_remap',
                                              input_bam=out_bam,
                                              output_bam=out_bam.split('.')[0]+'remapped.prepped.bam',
                                              logger=log)
    mark_duplicates.run()
    print('Your output file of interest is at {PATH}'.format(PATH=mark_duplicates.retrieve_output_path()))

def test_filter_remapped():
    log = SimpleLog()
    filter_remapped = RunWaspFilterRemappedReads(output_dir='tests/filter_remapped',
                                                  input_bam_to_remap='examples/smallAligned.RG.MG.to.remap.bam',
                                                  input_bam_remapped='examples/smallAligned.remapped.prepped.bam',
                                                  logger=log)
    filter_remapped.run()
    print('Your output file of interest is at {PATH}'.format(PATH=filter_remapped.retrieve_output_path()))


def test_samtools():
    log = SimpleLog()
    samtools = RunSamtools(logger=log)
    samtools.run()

def test_samtools_merge():
    log = SimpleLog()
    samtools_merge = RunSamtoolsMerge(output_dir='tests/samtools_merge',
                                      input_bam1='examples/smallAligned.remap.keep.bam',
                                      input_bam2='examples/smallAligned.RG.MG.keep.bam',
                                      logger=log)
    samtools_merge.run()
    print('Your output file of interest is at {PATH}'.format(PATH=samtools_merge.retrieve_output_path()))


def test_samtools_sort():
    log = SimpleLog()
    samtools_merge = RunSamtoolsSort(output_dir='tests/samtools_sort',
                                      input_bam='examples/smallAligned.merged.bam',
                                      logger=log)
    samtools_merge.run()
    print('Your output file of interest is at {PATH}'.format(PATH=samtools_merge.retrieve_output_path()))

def test_samtools_index():
    log = SimpleLog()
    samtools_index = RunSamtoolsIndex(input_bam='examples/smallAligned.sorted.bam',
                                     logger=log)
    samtools_index.run()


def test_ase_read_counter():
    log = SimpleLog()

    ase_read_counter = RunGATKASEReadCounter(output_dir='tests/ase_read_counter',
                                             input_bam='examples/smallAligned.sorted.bam',
                                             input_sites_vcf='examples/smallAligned.FILTERED.HET.vcf',
                                             logger=log)

    ase_read_counter.run()
    print('Your output file of interest is at {PATH}'.format(PATH=ase_read_counter.retrieve_output_path()))

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

    if which == 'rnaseq_var' or which == 'all':
        test_rnaseq_variant_calling_pipe()

    if which == 'filter_vcf' or which == 'all':
        test_filter_vcf()

    if which == 'make_wasp_snp_dir' or which == 'all':
        test_make_wasp_snp_dir()

    if which == 'find_intersecting_snps' or which == 'all':
        test_find_intersecting_snps()

    if which == 'star_remap' or which == 'all':
        test_star_remap()

    if which == 'prep_star_remap' or which == 'all':
        test_prep_star_remap()

    if which == 'filter_remapped' or which == 'all':
        test_filter_remapped()

    if which == 'samtools' or which == 'all':
        test_samtools()

    if which == 'samtools_merge' or which == 'all':
        test_samtools_merge()

    if which == 'samtools_sort' or which == 'all':
        test_samtools_sort()

    if which == 'samtools_index' or which == 'all':
        test_samtools_index()

    if which == 'ase_read_counter' or which == 'all':
        test_ase_read_counter()
