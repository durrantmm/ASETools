from os.path import join
import os
from mod.subprocess.add_read_groups import RunPicardAddReadGroups
from mod.subprocess.haplotype_caller import RunGATKHaplotypeCaller
from mod.subprocess.print_reads import RunGATKPrintReads
from mod.subprocess.rnaseq_base_recalibrator import RunGATKRNAseqBaseRecalibrator
from mod.subprocess.split_n_cigar_reads import RunGATKSplitNCigarReads
from mod.subprocess.star_align import RunStarAlign
from mod.subprocess.variant_filtration import RunGATKVariantFiltration

from mod.config.fixed import RNASeqVariantCallingFixedConfig
from mod.run_process_piped_super import RunProcessPipedSuper
from mod.subprocess.mark_duplicates import RunPicardMarkDuplicates


class RunAlignAddGroupsMarkDups(RunProcessPipedSuper):

    def __init__(self, output_dir, fastq1, fastq2, logger):
        fixed_config = RNASeqVariantCallingFixedConfig()

        name = fixed_config.name
        output_dir = output_dir

        input = fixed_config.input
        input.arg1 = fastq1
        input.arg2 = fastq2

        logger = logger

        super().__init__(name, output_dir, input, logger)

    def execute_steps(self):
        # STAR ALIGN
        star_output_dir = join(self.output_dir, 'STEP1_STAR_ALIGN')
        run_star = RunStarAlign(output_dir=star_output_dir,
                                fastq1=self.input.arg1,
                                fastq2=self.input.arg2,
                                logger=self.logger)
        run_star.run()
        star_output_sam = run_star.retrieve_output_path()

        # ADD READ GROUPS
        add_read_groups_output_dir = join(self.output_dir, "STEP2_ADD_READ_GROUPS")
        run_add_read_groups = RunPicardAddReadGroups(output_dir=add_read_groups_output_dir,
                                                     input_sam=star_output_sam,
                                                     logger=self.logger)
        run_add_read_groups.run()
        arg_output_bam = run_add_read_groups.retrieve_output_path()
        os.remove(star_output_sam)

        # MARK DUPLICATES
        mark_dups_output_dir = join(self.output_dir, "STEP3_MARK_DUPLICATES")
        mark_dups = RunPicardMarkDuplicates(output_dir = mark_dups_output_dir,
                                            input_bam=arg_output_bam,
                                            logger=self.logger)
        mark_dups.run()
        mark_dups_bam = mark_dups.retrieve_output_path()
        os.remove(arg_output_bam)





