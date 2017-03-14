import sys
from mod.misc.string_constants import *

parse_star_version = lambda x: x.decode(UTF8).strip()

parse_java_version = lambda x: x.decode(UTF8).split()[2].strip('\"')

parse_add_read_groups_version = lambda x, y: x.decode(UTF8).split()[x.decode(UTF8).split().index(y)]

parse_mark_duplicates_version = lambda x, y: x.decode(UTF8).split()[x.decode(UTF8).split().index(y)]

parse_gatk_version = lambda x: x.decode(UTF8).strip()


parse_samtools_version = lambda x: x.decode(UTF8).strip().split()[1]