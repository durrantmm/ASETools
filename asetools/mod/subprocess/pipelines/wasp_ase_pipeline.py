from os.path import join, isfile, isdir

from mod.subprocess.add_read_groups import RunPicardAddReadGroups
from mod.subprocess.ase_read_counter import RunGATKASEReadCounter
from mod.subprocess.mark_duplicates import RunPicardMarkDuplicates
from mod.subprocess.samtools_merge import RunSamtoolsMerge
from mod.subprocess.samtools_sort import RunSamtoolsSort
from mod.subprocess.star_align import RunStarAlign
from mod.subprocess.wasp_filter_remapped_reads import RunWaspFilterRemappedReads
from mod.subprocess.wasp_find_intersecting_snps import RunWaspFindIntersectingSnps

from mod.config.fixed import WASPAlleleSpecificExpressionPipelineFixedConfig
from mod.process.wasp_make_snp_dir import RunMakeWaspSnpDir
from mod.run_process_piped_super import RunProcessPipedSuper
from mod.subprocess.samtools_index import RunSamtoolsIndex


class WASPAlleleSpecificExpressionPipeline(RunProcessPipedSuper):

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


        # MAKE WASP SNP DIR
        snp_dir = join(self.output_dir, 'STEP%d_MAKE_SNP_DIR' % step_num)
        make_snp_dir = RunMakeWaspSnpDir(output_dir=snp_dir,
                                         input_sorted_vcf=self.input_vcf,
                                         logger=self.logger)

        make_snp_dir.run()
        step_num += 1

        # WASP - FIND INTERSECTING SNPS
        find_intersecting_snps_output_dir = join(self.output_dir, 'STEP%d_FIND_INTERSECTING_SNPS' % step_num)
        find_intersecting_snps = RunWaspFindIntersectingSnps(output_dir=find_intersecting_snps_output_dir,
                                                             input_bam=self.input_bam,
                                                             input_snp_dir=snp_dir,
                                                             logger=self.logger)

        find_intersecting_snps.run()
        step_num += 1

        bam_keep, bam_remap, fastq1_remap, fastq2_remap, fastq_single_remap = find_intersecting_snps.retrieve_output_path()

        # WASP - STAR REMAP
        star_remap_output_dir = join(self.output_dir, 'STEP%d_REMAP_OUTPUT_DIR' % step_num)
        star_remap = RunStarAlign(output_dir=star_remap_output_dir,
                                  fastq1=fastq1_remap,
                                  fastq2=fastq2_remap,
                                  logger=self.logger)
        star_remap.run()
        step_num += 1

        remap_sam = star_remap.retrieve_output_path()

        # STAR REMAP ADD READ GROUPS
        add_read_groups_output_dir = join(self.output_dir, "STEP%d_STAR_REMAP_ADD_READ_GROUPS" % step_num)
        run_star_remap_add_read_groups = RunPicardAddReadGroups(output_dir=add_read_groups_output_dir,
                                                                input_sam=remap_sam,
                                                                logger=self.logger)
        run_star_remap_add_read_groups.run()
        step_num += 1

        arg_output_bam = run_star_remap_add_read_groups.retrieve_output_path()


        # STAR REMAP MARK DUPLICATES
        mark_dups_output_dir = join(self.output_dir, "STEP%d_STAR_REMAP_MARK_DUPLICATES" % step_num)
        star_remap_mark_dups = RunPicardMarkDuplicates(output_dir=mark_dups_output_dir,
                                                       input_bam=arg_output_bam,
                                                       logger=self.logger)
        star_remap_mark_dups.run()
        step_num += 1

        self.input_bam = star_remap_mark_dups.retrieve_output_path()

        # WASP - FILTER REMAP
        filter_remapped_output_dir = join(self.output_dir, "STEP%d_WASP_FILTER_REMAPPED" % step_num)
        filter_remapped = RunWaspFilterRemappedReads(output_dir=filter_remapped_output_dir,
                                                     input_bam_to_remap=bam_remap,
                                                     input_bam_remapped=self.input_bam,
                                                     logger=self.logger)
        filter_remapped.run()
        step_num += 1

        remapped_output_bam = filter_remapped.retrieve_output_path()

        # SAMTOOLS MERGE
        samtools_merge_output_dir = join(self.output_dir, "STEP%d_MERGE_WASP_BAMS" % step_num)
        samtools_merge = RunSamtoolsMerge(output_dir=samtools_merge_output_dir,
                                          input_bam1=remapped_output_bam,
                                          input_bam2=bam_keep,
                                          logger=self.logger)
        samtools_merge.run()
        step_num += 1
        merged_bam = samtools_merge.retrieve_output_path()

        # SAMTOOLS SORT
        samtools_sort_output_dir = join(self.output_dir, "STEP%d_SORT_BAM" % step_num)
        samtools_sort = RunSamtoolsSort(output_dir=samtools_sort_output_dir,
                                         input_bam=merged_bam,
                                         logger=self.logger)
        samtools_sort.run()
        step_num += 1
        sorted_bam = samtools_sort.retrieve_output_path()

        # SAMTOOLS INDEX
        samtools_index = RunSamtoolsIndex(input_bam=sorted_bam,
                                          logger=self.logger)
        samtools_index.run()

        # ASE READ COUNTER
        ase_read_counter_output_dir = join(self.output_dir, "STEP%d_ASE_READ_COUNTER" % step_num)
        ase_read_counter = RunGATKASEReadCounter(output_dir=ase_read_counter_output_dir,
                                                 input_bam=sorted_bam,
                                                 input_sites_vcf=self.input_vcf,
                                                 logger=self.logger)
        ase_read_counter.run()










