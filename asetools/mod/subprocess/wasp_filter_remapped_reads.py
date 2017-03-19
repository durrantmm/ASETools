import subprocess
from os.path import basename, join

from mod.config.custom import WASPFilterRemappedReadsCustomConfig

from mod.config.fixed import WASPFilterRemappedReadsFixedConfig
from mod.misc.log import *
from mod.misc.record_classes import *
from mod.misc.string_constants import *
from mod.run_subprocess_step_superclass import RunSubprocessStepSuper


class RunWaspFilterRemappedReads(RunSubprocessStepSuper):

    def __init__(self, output_dir, input_bam_to_remap, input_bam_remapped, output_bam=None, logger=None):

        custom_config = WASPFilterRemappedReadsCustomConfig()
        fixed_config = WASPFilterRemappedReadsFixedConfig()

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
        input.arg1 = input_bam_to_remap
        input.arg2 = input_bam_remapped
        output.arg = self.handle_output_bam(output_bam, input_bam_to_remap)

        super().__init__(name=name, output_dir=output_dir, execution_path=execution_path, version=version,
                         version_flag=version_flag, version_parser=version_parser, input=input,
                         output=output, args=args, log_name=log_name, logger=logger)


    def handle_output_bam(self, output_bam, input_bam):
        if output_bam:
            return basename(output_bam)
        else:
            return basename(input_bam).split('.')[0]+'.remap.keep.bam'

    def format_command(self):

        command = [self.execution_path, self.input.arg1, self.input.arg2, join(self.output_dir, self.output.arg)]

        return SPACE.join(command)

    def execute_command(self, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False):
        command = self.format_command()
        Log.info_chk(self.logger, msg_executing_command.format(DELIM=NL, COMMAND=command))
        Log.debug_chk(self.logger, msg_execute_command_signature.format(STDERR=stderr, SHELL=shell))

        subprocess.check_call(command, shell=True, universal_newlines=True)


    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parser=False):
        pass

    def get_log_json(self, input_class_parse=FlagArg_to_tuple, output_class_parse=FlagArg_to_tuple):
        super().get_log_json(input_class_parse=FlagTwoArgs_to_tuple)

