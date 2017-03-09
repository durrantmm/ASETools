#!/usr/bin/env python3

import sys
from os.path import basename, splitext
import importlib.machinery
import subprocess
import argparse

STAR_VERSION_ERROR = "The STAR aligner is version {ACTUAL}, not {EXPECTED}, as specified in the config file."


def main(config):
    align_reads_with_STAR(config)

def align_reads_with_STAR(config):
    check_star_version(config.StarAligner.PATH, config.StarAligner.VERSION)

def check_star_version(star_path, version, version_flag="--version"):
    global STAR_VERSION_ERROR
    stdout = subprocess.check_output([star_path, version_flag]).strip()
    print(stdout)
    local_version = stdout.strip()
    assert version == local_version, STAR_VERSION_ERROR.format(ACTUAL=local_version, EXPECTED=version)


if __name__ == "__main__":
    config_path = sys.argv[1]
    config_module_name = splitext(basename(config_path))[0]

    config = importlib.machinery.SourceFileLoader(config_module_name, config_path).load_module().Config

    main(config)
