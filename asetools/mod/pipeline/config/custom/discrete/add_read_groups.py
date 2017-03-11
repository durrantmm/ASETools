from mod.pipeline.execute_step_super import ExecutionStepSuper
from mod.pipeline.config.custom.discrete.java import CustomConfigJava
from mod.misc.string_constants import *



class CustomConfigAddReadGroups(ExecutionStepSuper):

    def __init__(self):
        super().__init__()

        self.java = CustomConfigJava()

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
