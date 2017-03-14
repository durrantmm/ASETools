import sys
from os.path import join, basename
from mod.pipeline.run_process.run_process_piped_super import RunProcessPipedSuper
from mod.pipeline.run_python.steps.make_wasp_snp_dir import RunMakeWaspSnpDir
from mod.pipeline.run_process.steps.wasp_find_intersecting_snps import RunWaspFindIntersectingSnps
from mod.pipeline.run_process.steps.star_align import RunStarAlign

class WASPBiasRemoval(RunProcessPipedSuper):

    def __init__(self, output_dir, input_bam, input_vcf, logger):


        name = "WASP-BiasRemovalPipeline"
        output_dir = output_dir

        input = None

        logger = logger

        super().__init__(name, output_dir, input, logger)

        self.input_bam = input_bam
        self.input_vcf = input_vcf

    def execute_steps(self):
        # MAKE SNP DIR
        make_snp_dir_output = join(self.output_dir, 'STEP1_MAKE_SNP_DIR')
        make_snp_dir = RunMakeWaspSnpDir(output_dir=make_snp_dir_output,
                                     input_sorted_vcf=self.input_vcf,
                                     logger=self.logger)

        make_snp_dir.run()
        snp_directory = make_snp_dir.retrieve_output_path()

        # FIND INTERSECTING SNPS
        find_intersecting_snps_output_dir = join(self.output_dir, "STEP2_FIND_INTERSECTING_SNPS")
        find_intersecting_snps = RunWaspFindIntersectingSnps(output_dir=find_intersecting_snps_output_dir,
                                                            input_bam=self.input_bam,
                                                            input_snp_dir=snp_directory,
                                                            logger=self.logger())
        find_intersecting_snps.run()
        bam_keep, bam_remap, fastq1_remap, fastq2_remap, fastq_single_remap = find_intersecting_snps.retrieve_output_path()

        # STAR ALIGN
        star_output_dir = join(self.output_dir, 'STEP3_STAR_REALIGN')
        run_star = RunStarAlign(output_dir=star_output_dir,
                                fastq1=fastq1_remap,
                                fastq2=fastq2_remap,
                                logger=self.logger)
        run_star.run()
        star_output_sam = run_star.retrieve_output_path()





