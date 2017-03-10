from recordclass import recordclass

##### Simple record class to store flag and arg
FlagArg = recordclass('FlagArg', 'flag, arg')
def FlagArg_to_tuple(flagarg):
    return (flagarg.flag, flagarg.arg)


##### Record Class to specify Flag with two arguments
FlagTwoArgs = recordclass('FlagTwoArgs', 'flag, arg1, arg2')
def FlagTwoArgs_to_tuple(flagtwoargs):
    return (flagtwoargs.flag, flagtwoargs.arg1, flagtwoargs.arg2)