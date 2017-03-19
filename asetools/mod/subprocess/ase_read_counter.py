import subprocess
from os.path import basename, join

from mod.config.custom import GATKASEReadCounterCustomConfig

from mod.config.fixed import GATKASEReadCounterFixedConfig
from mod.misc.string_constants import *
from mod.run_subprocess_step_superclass import RunSubprocessStepSuper
from mod.subprocess.java import RunJava


class RunGATKASEReadCounter(RunSubprocessStepSuper):

    def __init__(self, output_dir, input_bam, input_sites_vcf, output_counts=None, logger=None):

        custom_config = GATKASEReadCounterCustomConfig()
        fixed_config = GATKASEReadCounterFixedConfig()

        name = fixed_config.name
        output_dir = output_dir
        execution_path = custom_config.execution_path

        version = custom_config.version
        version_flag = custom_config.version_flag
        version_parser = fixed_config.version_parser

        input = fixed_config.input
        input_sites = fixed_config.input_sites
        output = fixed_config.output

        args = custom_config.args

        log_name = fixed_config.log_name
        logger = logger

        # Adjusting attributes based on relevant input variables
        input.arg = input_bam
        input_sites.arg = input_sites_vcf
        output.arg = self.handle_output_counts(output_counts, input_bam)


        # Adding a java step to check its version
        self.java = RunJava(logger=logger)
        self.input_sites = input_sites

        super().__init__(name=name, output_dir=output_dir, execution_path=execution_path, version=version,
                         version_flag=version_flag, version_parser=version_parser, input=input,
                         output=output, args=args, log_name=log_name, logger=logger)




    def handle_output_counts(self, output_counts, input_bam):
        if output_counts:
            return basename(output_counts)
        else:
            output_vcf = basename(input_bam).split('.')[0] + '.tsv'
            return basename(output_vcf)


    def format_command(self):

        command = [self.execution_path, SPACE.join([self.input.flag, self.input.arg]),
                   SPACE.join([self.input_sites.flag, self.input_sites.arg]),
                   SPACE.join([self.output.flag, join(self.output_dir, self.output.arg)])]
        command.extend([SPACE.join(map(str, [flag, arg])) for flag, arg in self.args])

        return SPACE.join(command)


    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parse=False):
        self.java.check_version()
        super().check_version()