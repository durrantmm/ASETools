import sys

from mod.misc.log import SimpleLog
from mod.pipeline.run.steps.star_align import RunStarAlign
from mod.pipeline.run.steps.add_read_groups import RunPicardAddReadGroups
from mod.pipeline.run.steps.mark_duplicates import RunPicardMarkDuplicates


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

    mark_duplicates = RunPicardMarkDuplicates(output_dir='tests/add_mark_duplicates_test1',
                                               input_bam='examples/smallAligned.RG.bam',
                                               output_bam='examples/smallAligned.RG.MG.bam',
                                               logger=log)
    mark_duplicates.run()
    print('Your output file of interest is at {PATH}'.format(PATH=mark_duplicates.retrieve_output_path()))


def test_split_n_cigar_reads():
    log = SimpleLog()

    split_reads = RunPicardMarkDuplicates(output_dir='tests/add_split_reads_test1',
                                          input_bam='examples/smallAligned.RG.MG.bam',
                                          output_bam='examples/smallAligned.RG.MG.SPLIT.bam',
                                          logger=log)

    split_reads.run()
    print('Your output file of interest is at {PATH}'.format(PATH=split_reads.retrieve_output_path()))



if __name__ == '__main__':

    which = sys.argv[1]

    if which == 'star_align':
        test_star_align()

    if which == 'add_read_groups':
        test_add_read_groups()

    if which == 'mark_duplicates':
        test_mark_duplicates()

    if which == 'split_reads':
        test_split_n_cigar_reads()

