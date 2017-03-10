import sys
from mod.pipeline.run.star_align import RunStarAlign

def test_star_align():
    star_align = RunStarAlign('star_align_output_dir', 'examples/small.1.fastq', 'examples/small.2.fastq')
    star_align.run()


if __name__ == '__main__':

    which = sys.argv[1]

    if which == 'star_align':
        test_star_align()

