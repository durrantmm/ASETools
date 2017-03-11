from collections import OrderedDict
from mod.pipeline.execute_step_super import ExecutionStepSuper

class CustomConfigStarAlign(ExecutionStepSuper):

    def __init__(self):
        super().__init__()
        # Path to the star aligner, absolute path is preferred over aliases
        self.execution_path = "/home/mdurrant/miniconda3/bin/STAR"
        # The version of STAR aligner. Change at your own risk.
        # These are the options for the STAR alignment command
        # If the argument is optional, set its value to None to exclude.
        self.version = "STAR_2.5.2b"
        self.version_flag = '--version'

        self.args = [

            ("--genomeDir", "/srv/gsfs0/projects/bhatt/mdurrant/BUTYRATE_brayon/references/starGenomeUCSChg19"),
            ("--readFilesCommand", "zcat"),
            ("--runThreadN", 2),
            ("--genomeLoad", "NoSharedMemory"),
            ("--outFilterMultimapNmax", 20),
            ("--alignSJDBoverhangMin", 1),
            ("--outFilterMultimapNmax", 999),
            ("--outFilterMismatchNoverReadLmax", 0.04),
            ("--alignIntronMin", 20),
            ("--alignIntronMax", 1000000),
            ("--alignMatesGapMax", 1000000),
            ("--outSAMunmapped", "Within"),
            ("--outFilterType", "BySJout"),
            ("--outSAMattributes", "NH HI AS NM MD"),
            ("--sjdbScore", 1),
            ("--twopassMode", "Basic"),
            ("--twopass1readsN", -1)

        ]