"""
This script contains functions that ensure that certaio argparse arguments are formatted correctly.
This will likely be added to later as the asetools package is expanded.
"""


import argparse
import os


ref_basenames = set()

def cases_controls(cases, controls):
    """
    Validates the cases and controls arguments for the PrepareCountData protocol.
    :param cases: The cases as passed into asetools.
    :param controls: The controls as passed into asetools.
    :return:
    """

    # This guarantees that for each set of cases there is a corresponding set of controls
    if len(cases) != len(controls):
        raise argparse.ArgumentTypeError("Each set of cases must have a matching set of controls. For example: "
                                         "--cases CASE1.1 CASE1.2 CASE1.3 --controls CONTROL1.1 CONTROL1.2 --cases "
                                         "CASE2.1 CASE2.2 --controls CONTROL2.1 CONTROL2.2 CONTROL2.3")

    # This checks to make sure that all of the given case tsv files are valid
    for treatment in cases:
        for case in treatment:
            if not os.path.isfile(case):
                raise argparse.ArgumentTypeError('You must give valid paths to read count tsv files - INVALID: %s' %
                                                 case)

    # This checks to make sure that all of the give, control tsv files are valid
    for treatment in controls:
        for control in treatment:
            if not os.path.isfile(control):
                raise argparse.ArgumentTypeError('You must give valid paths to read count tsv files - INVALID: %s' %
                                                 control)