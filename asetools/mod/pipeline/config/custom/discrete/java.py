from mod.pipeline.execute_step_super import ExecutionStepSuper



class CustomConfigJava(ExecutionStepSuper):

    def __init__(self):
        super().__init__()
        self.execution_path = "/srv/gs1/software/java/jre1.8.0_66/bin/java"
        self.version = "1.8.0_66"
        self.version_flag = "-version"