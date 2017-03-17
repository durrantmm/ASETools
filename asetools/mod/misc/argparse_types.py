import argparse
import os, sys

ref_basenames = set()

def cases_controls(cases, controls):

    if len(cases) != len(controls):
        raise argparse.ArgumentTypeError("Each set of cases must have a matching set of controls. For example: "
                                         "--cases CASE1.1 CASE1.2 CASE1.3 --controls CONTROL1.1 CONTROL1.2 --cases "
                                         "CASE2.1 CASE2.2 --controls CONTROL2.1 CONTROL2.2 CONTROL2.3")
    for treatment in cases:
        for case in treatment:
            if not os.path.isfile(case):
                raise argparse.ArgumentTypeError('You must give valid paths to read count tsv files - INVALID: %s' %
                                                 case)

    for treatment in controls:
        for control in treatment:
            if not os.path.isfile(control):
                raise argparse.ArgumentTypeError('You must give valid paths to read count tsv files - INVALID: %s' %
                                                 control)

