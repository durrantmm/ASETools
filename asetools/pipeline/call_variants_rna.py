#!/usr/bin/env python3

import sys
from os.path import basename, splitext
import importlib.machinery
import subprocess
import argparse

STAR_VERSION_ERROR = "The STAR aligner is version {ACTUAL}, not {EXPECTED}, as specified in the config file."
tab = '\t'
whitespace = ' '
new_line = '\n'
utf8 = "utf-8"


def main(config):
    align_reads_with_STAR(config)

def align_reads_with_STAR(config):
    global whitespace
    check_star_version(config.StarAligner.PATH, config.StarAligner.VERSION)
    star_command_args = convert_iters_to_string_recursive(config.StarAligner.STAR_COMMAND_DICT.items())
    star_command = whitespace.join([config.StarAligner.PATH, star_command_args])
    print(star_command)


# Version Checks
def check_star_version(star_path, version, version_flag="--version"):
    global STAR_VERSION_ERROR, utf8
    local_version = subprocess.check_output([star_path, version_flag]).decode(utf8).strip()
    assert version == local_version, STAR_VERSION_ERROR.format(ACTUAL=local_version, EXPECTED=version)

# Misc functions
def convert_iters_to_string_recursive(iterable, delim=whitespace):
    try:
        return delim.join(iterable)
    except TypeError:
        return delim.join(map(convert_iters_to_string_recursive, iterable))

if __name__ == "__main__":
    config_path = sys.argv[1]
    config_module_name = splitext(basename(config_path))[0]

    config = importlib.machinery.SourceFileLoader(config_module_name, config_path).load_module().Config

    main(config)


