from os.path import join, isfile, isdir

from mod.subprocess.add_read_groups import RunPicardAddReadGroups
from mod.subprocess.ase_read_counter import RunGATKASEReadCounter
from mod.subprocess.mark_duplicates import RunPicardMarkDuplicates
from mod.subprocess.star_align import RunStarAlign

from mod.config.fixed import WASPAlleleSpecificExpressionPipelineFixedConfig
from mod.run_process_piped_super import RunProcessPipedSuper


class RunAlleleSpecificExpressionPipeline(RunProcessPipedSuper):

    def __init__(self, output_dir, input_vcf, input_bam=None, fastq1=None, fastq2=None, logger=None):
        fixed_config = WASPAlleleSpecificExpressionPipelineFixedConfig()

        name = fixed_config.name
        output_dir = output_dir

        input = fixed_config.input
        input.arg1 = fastq1
        input.arg2 = fastq2

        logger = logger

        super().__init__(name, output_dir, input, logger)

        self.input_bam = input_bam
        self.input_vcf = input_vcf

    def execute_steps(self):
        step_num = 1

        if not self.input_bam:
            # STAR ALIGN
            star_output_dir = join(self.output_dir, 'STEP%d_STAR_ALIGN' % step_num)
            run_star = RunStarAlign(output_dir=star_output_dir,
                                    fastq1=self.input.arg1,
                                    fastq2=self.input.arg2,
                                    logger=self.logger)
            run_star.run()
            step_num += 1
            star_output_sam = run_star.retrieve_output_path()


            # ADD READ GROUPS
            add_read_groups_output_dir = join(self.output_dir, "STEP%d_ADD_READ_GROUPS" % step_num)
            run_add_read_groups = RunPicardAddReadGroups(output_dir=add_read_groups_output_dir,
                                                         input_sam=star_output_sam,
                                                         logger=self.logger)
            run_add_read_groups.run()
            step_num += 1
            arg_output_bam = run_add_read_groups.retrieve_output_path()


            # MARK DUPLICATES
            mark_dups_output_dir = join(self.output_dir, "STEP%d_MARK_DUPLICATES" % step_num)
            mark_dups = RunPicardMarkDuplicates(output_dir = mark_dups_output_dir,
                                                input_bam=arg_output_bam,
                                                logger=self.logger)
            mark_dups.run()
            step_num += 1
            self.input_bam = mark_dups.retrieve_output_path()


        # ASE READ COUNTER
        ase_read_counter_output_dir = join(self.output_dir, "STEP%d_ASE_READ_COUNTER" % step_num)
        ase_read_counter = RunGATKASEReadCounter(output_dir=ase_read_counter_output_dir,
                                                 input_bam=self.input_bam,
                                                 input_sites_vcf=self.input_vcf,
                                                 logger=self.logger)
        ase_read_counter.run()










