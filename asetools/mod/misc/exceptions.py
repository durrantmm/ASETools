import sys


class VersionError(Exception):
    def __init__(self, program, expected_version, observed_version):
        self.message = "Specified {PROGRAM} is version {OBSERVED}, not {EXPECTED} as specified".format(
            PROGRAM = program, OBSERVED = observed_version, EXPECTED = expected_version
        )

class ExecutionNotRanNoOutput(Exception):
    def __init__(self, program):
        self.message = "The program {PROGRAM} has not yet been executed. No output path available.".format(
            PROGRAM=program
        )
