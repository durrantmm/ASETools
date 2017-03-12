from mod.misc.string_constants import *
from mod.pipeline.run_step_super import RunStepSuper
from mod.pipeline.config.discrete.java import CustomConfigJava
from mod.misc.record_classes import FlagArg


class ConfigAddReadGroups(RunStepSuper):

    def __init__(self):
        self.name = name
        self.output_dir = output_dir
        self.execution_path = execution_path

        self.version = version
        self.version_flag = version_flag
        self.version_parser = version_parser
        self.args = args

        self.input = input
        self.output = output
        self.log_name = log_name

        self.logger = logger

        self.name = "AddOrReplaceReadGroups"

        self.input = FlagArg(flag='I', arg=None)

        self.output = FlagArg(flag='O', arg=None)

        # JSON File Name
        self.log_name = "add_read_groups.json"

        self.java_config = CustomConfigJava()

        self.execution_path = SPACE.join([self.java.execution_path, '-jar',
                                          "/srv/gs1/software/picard-tools/2.8.0/picard.jar",
                                          "AddOrReplaceReadGroups"])

        self.version = "2.8.0-SNAPSHOT"
        self.version_flag = "--help"

        self.args = [

            ("SO", "coordinate"),
            ("RGID", "id"),
            ("RGLB", "library"),
            ("RGPL", "platform"),
            ("RGPU", "machine"),
            ("RGSM", "sample")

        ]