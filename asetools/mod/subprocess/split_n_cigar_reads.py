import subprocess
from os.path import basename, join

from mod.subprocess.config.custom import GATKSplitNCigarReadsCustomConfig

from mod.config.fixed import GATKSplitNCigarReadsFixedConfig
from mod.misc.string_constants import *
from mod.run_process_step_super import RunProcessStepSuper
from mod.subprocess.java import RunJava


class RunGATKSplitNCigarReads(RunProcessStepSuper):

    def __init__(self, output_dir, input_bam, output_bam = None, logger=None):

        custom_config = GATKSplitNCigarReadsCustomConfig()
        fixed_config = GATKSplitNCigarReadsFixedConfig()

        name = fixed_config.name
        output_dir = output_dir
        execution_path = custom_config.execution_path

        version = custom_config.version
        version_flag = custom_config.version_flag
        version_parser = fixed_config.version_parser

        input = fixed_config.input
        output = fixed_config.output

        args = custom_config.args

        log_name = fixed_config.log_name
        logger = logger

        # Adjusting attributes based on relevant input variables
        input.arg = input_bam
        output.arg = self.handle_output_bam(output_bam, input_bam)

        # Adding a java step to check its version
        self.java = RunJava(logger=logger)

        super().__init__(name=name, output_dir=output_dir, execution_path=execution_path, version=version,
                         version_flag=version_flag, version_parser=version_parser, input=input,
                         output=output, args=args, log_name=log_name, logger=logger)


    def handle_output_bam(self, output_bam, input_sam):
        if output_bam:
            return basename(output_bam)
        else:
            output_bam = basename(input_sam).split('.')[0] + '.bam'
            return basename(output_bam)


    def format_command(self):

        command = [self.execution_path, SPACE.join([self.input.flag, self.input.arg]),
                   SPACE.join([self.output.flag, join(self.output_dir, self.output.arg)])]
        command.extend([SPACE.join(map(str, [flag, arg])) for flag, arg in self.args])

        return SPACE.join(command)


    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parse=False):
        self.java.check_version()
        super().check_version()