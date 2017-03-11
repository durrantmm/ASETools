import sys
from mod.pipeline.run.star_align import RunStarAlign
from mod.misc.log import SimpleLog

def test_star_align():
    log = SimpleLog()
    star_align = RunStarAlign('tests/star_align_output_dir', 'examples/small.1.fastq', 'examples/small.2.fastq', log)
    star_align.run()
    print('Your output file of interest is at {PATH}'.format(PATH=star_align.retrieve_output_path()))


if __name__ == '__main__':

    which = sys.argv[1]

    if which == 'star_align':
        test_star_align()

