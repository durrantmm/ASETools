from mod.pipeline.config.custom.discrete.add_read_groups import CustomConfigAddReadGroups
from mod.misc.record_classes import FlagArg, FlagTwoArgs

class FixedConfigAddReadGroups(CustomConfigAddReadGroups):

    def __init__(self):
        super().__init__()
        self.name = "AddOrReplaceReadGroups"

        self.input = FlagArg(flag='I', arg1=None)

        self.output = FlagArg(flag='O', arg=None)

        # JSON File Name
        self.log_name = "add_read_groups.json"