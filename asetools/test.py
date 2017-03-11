import sys

from mod.misc.log import SimpleLog
from mod.pipeline.run.discrete.star_align import RunStarAlign
from mod.pipeline.run.discrete.add_read_groups import RunAddReadGroups


def test_star_align():
    log = SimpleLog()
    star_align = RunStarAlign('tests/star_align_output_dir', 'examples/small.1.fastq', 'examples/small.2.fastq',
                              logger=log)
    star_align.run()
    print('Your output file of interest is at {PATH}'.format(PATH=star_align.retrieve_output_path()))


def test_add_read_groups():
    log = SimpleLog()
    add_read_groups = RunAddReadGroups('tests/add_read_groups_output_dir', 'examples/smallAligned.out.sam',
                                       logger=log)
    add_read_groups.run()
    print('Your output file of interest is at {PATH}'.format(PATH=add_read_groups.retrieve_output_path()))

if __name__ == '__main__':

    which = sys.argv[1]

    if which == 'star_align':
        test_star_align()

    if which == 'add_read_groups':
        test_add_read_groups()

