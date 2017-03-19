"""
AUTHOR: Matt Durrant

This is used for storing recordclass objects, which are lightweight objects that can be accessed by property
and they are mutable.
"""

from recordclass import recordclass

# Simple record class to store flag and arg
FlagArg = recordclass('FlagArg', 'flag, arg')


def flagarg_to_tuple(flagarg):
    return flagarg.flag, flagarg.arg


# Record Class to specify Flag with two arguments
FlagTwoArgs = recordclass('FlagTwoArgs', 'flag, arg1, arg2')


def flagtwoargs_to_tuple(flagtwoargs):
    return flagtwoargs.flag, flagtwoargs.arg1, flagtwoargs.arg2
