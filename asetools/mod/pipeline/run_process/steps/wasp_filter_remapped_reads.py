from glob import glob
from os.path import basename, join
import os
import subprocess

from mod.misc.log import *
from mod.misc.record_classes import FlagArg
from mod.misc.string_constants import *
from mod.pipeline.config.custom import WASPFilterRemappedReadsCustomConfig
from mod.pipeline.config.fixed import WASPFilterRemappedReadsFixedConfig
from mod.pipeline.run_process.run_process_step_super import RunProcessStepSuper


class RunWaspFilterRemappedReads    (RunProcessStepSuper):

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
        input.arg2 = input_bam_to_remap
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

        command = [self.execution_path]
        command.extend([SPACE.join(map(str, [flag, arg])) for flag, arg in self.args])
        command.extend([self.output.flag, self.output.arg])
        command.extend([self.input_snp_dir.flag, self.input_snp_dir.arg])
        command.append(self.input.arg)

        return SPACE.join(command)

    def retrieve_output_path(self, default_output=True):
        print(glob(self.output_dir+os.sep+AST+'keep.bam'))
        print(self.output_dir+os.sep+AST+'to.keep.bam')
        bam_keep = glob(self.output_dir+os.sep+AST+'keep.bam').pop()
        bam_remap = glob(self.output_dir+os.sep+AST+'to.remap.bam').pop()
        fastq1_remap = glob(self.output_dir+os.sep+AST+'fq1.gz').pop()
        fastq2_remap = glob(self.output_dir + os.sep + AST + 'fq2.gz').pop()
        fastq_single_remap = glob(self.output_dir + os.sep + AST + 'single.fq.gz').pop()

        return bam_keep, bam_remap, fastq1_remap, fastq2_remap, fastq_single_remap

    def execute_command(self, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False):
        command = self.format_command()
        Log.info_chk(self.logger, msg_executing_command.format(DELIM=NL, COMMAND=command))
        Log.debug_chk(self.logger, msg_execute_command_signature.format(STDERR=stderr, SHELL=shell))

        subprocess.check_call(command, shell=True, universal_newlines=True)


    def check_version(self, stderr=subprocess.PIPE, ignore_error=False, pass_version_to_parser=False):
        pass

