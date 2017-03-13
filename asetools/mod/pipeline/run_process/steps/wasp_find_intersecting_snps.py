from glob import glob
from os.path import basename, join
import subprocess

from mod.misc.record_classes import FlagArg
from mod.misc.path_methods import get_shared_prefix
from mod.misc.record_classes import FlagTwoArgs_to_tuple
from mod.misc.string_constants import *
from mod.pipeline.config.custom import WASPFindIntersectingSnpsCustomConfig
from mod.pipeline.config.fixed import WASPFindIntersectingSnpsFixedConfig
from mod.pipeline.run_process.run_process_step_super import RunProcessStepSuper


class RunWaspFindIntersectingSnps(RunProcessStepSuper):

    def __init__(self, output_dir, input_bam, input_snp_dir, output_bam=None, logger=None):

        custom_config = WASPFindIntersectingSnpsCustomConfig()
        fixed_config = WASPFindIntersectingSnpsFixedConfig()

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
        output.arg = output_dir

        super().__init__(name=name, output_dir=output_dir, execution_path=execution_path, version=version,
                         version_flag=version_flag, version_parser=version_parser, input=input,
                         output=output, args=args, log_name=log_name, logger=logger)

        self.input_snp_dir = FlagArg(flag='--snp_dir', arg=input_snp_dir)



    def format_command(self):

        command = [self.execution_path]
        command.extend([SPACE.join(map(str, [flag, arg])) for flag, arg in self.args])
        command.extend([self.output.flag, self.output.arg])
        command.extend([self.input_snp_dir.flag, self.input_snp_dir.arg])
        command.append(self.input.arg)

        return SPACE.join(command)


    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parser=False):
        pass
