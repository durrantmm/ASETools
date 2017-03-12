import sys

from mod.misc.log import SimpleLog
from mod.pipeline.run.steps.star_align import RunStarAlign
from mod.pipeline.run.steps.add_read_groups import RunPicardAddReadGroups


def test_star_align():
    log = SimpleLog()
    star_align = RunStarAlign(output_dir='tests/star_align_test1',
                              fastq1='examples/small.1.fastq',
                              fastq2='examples/small.2.fastq',
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



if __name__ == '__main__':

    which = sys.argv[1]

    if which == 'star_align':
        test_star_align()

    if which == 'add_read_groups':
        test_add_read_groups()

