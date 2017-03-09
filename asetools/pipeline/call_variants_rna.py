#!/usr/bin/env python3

import sys, os
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
    check_star_version(config.StarAligner.PATH, config.StarAligner.VERSION)
    star_command_args = format_command_args(config.StarAligner.STAR_COMMAND_DICT)
    star_command = whitespace.join([config.StarAligner.PATH, star_command_args])
    print(star_command)


# Version Checks
def check_star_version(star_path, version, version_flag="--version"):
    local_version = subprocess.check_output([star_path, version_flag]).decode(utf8).strip()
    assert version == local_version, STAR_VERSION_ERROR.format(ACTUAL=local_version, EXPECTED=version)


# Misc functions
def format_command_args(command_args, delim=whitespace):
    out_command = []
    for key, value in command_args.items():
        if not value:
            continue
        if isinstance(value, list) or isinstance(value, set):
            out_command.append(delim.join(map(str, [key, delim.join(map(str, value))])))
        else:
            out_command.append(delim.join(map(str, [key, value])))
    return delim.join(out_command)


def contains_iterable(iterable):
    if not iterable:
        return False

    if isinstance(iterable, str):
        return False

    if not hasattr(iterable, '__iter__'):
        return False

    for item in iterable:
        if hasattr(iterable, '__iter__'):
            return True

    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('config', type=str,
                        help='The config.py file to use in the pipeline.')
    parser.add_argument('-oSTAR', '--override_star_argument', action="append",
                        help="Onlye one new argument per use of option. "
                             "Example: -oSTAR \"--readFilesIn paired_ends.1.fq.gz paired_ends.2.fq.gz\""
                             "-oSTAR \"--out1FileNamePrefix paired_end_alignment\"")

    args = vars(parser.parse_args())

    config_path = args['config']
    config_module_name = splitext(basename(config_path))[0]

    config = importlib.machinery.SourceFileLoader(config_module_name, config_path).load_module().Config

    if args["override_star_argument"]:
        for entry in args["override_star_argument"]:
            flag, argument = entry.split()[0], whitespace.join(entry.split()[1:])
            config.StarAligner.STAR_COMMAND_DICT[flag] = argument

    main(config)


