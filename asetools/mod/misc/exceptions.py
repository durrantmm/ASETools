import sys

# This module stores all of the exceptions that are used to handle errors that can occur throughout the application.


class VersionError(Exception):
    """
    This is a simple error class used to handle software version errors.
    """

    def __init__(self, program, expected_version, observed_version):
        super().__init__("Specified {PROGRAM} is version {OBSERVED}, not {EXPECTED} as specified".format(
            PROGRAM = program, OBSERVED = observed_version, EXPECTED = expected_version
        ))

class ExecutionNotRanNoOutput(Exception):
    """
    This is a class used to handle the case where a given operation, such as add read groups or mark duplicates,
    has been queried to return the output file before the operation has even run.
    """
    def __init__(self, program):
        super().__init__("The program {PROGRAM} has not yet been executed. No output path available.".format(
            PROGRAM=program
        ))
