#!/usr/bin/env python3
from collections import OrderedDict

class Config:
    # General reference genome in fasta format. For example, ucsc.hg19.fasta
    REFERENCE_GENOME_PATH = "/srv/gsfs0/projects/bhatt/mdurrant/BUTYRATE_brayon/references/hg19/ucsc.hg19.fasta"
    
    class StarAligner:
    
        # Path to the star aligner, absolute path is preferred over aliases
        PATH = "/home/mdurrant/miniconda3/bin/STAR"
        # The version of STAR aligner. Change at your own risk.
        VERSION = "STAR_2.5.2b"
    
        # These are the options for the STAR alignment command
        # If the argument is optional, set its value to None to exclude.
        VERSION_FLAG = '--version'
    
        genomeDir_FLAG = "--genomeDir"
        genomeDir_ARG = "/srv/gsfs0/projects/bhatt/mdurrant/BUTYRATE_brayon/references/starGenomeUCSChg19"
    
        readFilesIn_FLAG = "--readFilesIn"
        readFilesIn_ARG = None
    
        readFilesCommand_FLAG = "--readFilesCommand"
        readFilesCommand_ARG = "zcat"
    
        runThreadN_FLAG = "--runThreadN"
        runThreadN_ARG = 2
    
        genomeLoad_FLAG = "--genomeLoad"
        genomeLoad_ARG = "NoSharedMemory"
    
        outFilterMultimapNmax_FLAG = "--outFilterMultimapNmax"
        outFilterMultimapNmax_ARG = 20
    
        alignSJDBoverhangMin_FLAG = "--alignSJDBoverhangMin"
        alignSJDBoverhangMin_ARG = 1
    
        outFilterMismatchNmax_FLAG = "--outFilterMultimapNmax"
        outFilterMismatchNmax_ARG = 999
    
        outFilterMismatchNoverReadLmax_FLAG = "--outFilterMismatchNoverReadLmax"
        outFilterMismatchNoverReadLmax_ARG = 0.04
    
        alignIntronMin_FLAG = "--alignIntronMin"
        alignIntronMin_ARG = 20
    
        alignIntronMax_FLAG = "--alignIntronMax"
        alignIntronMax_ARG = 1000000
    
        alignMatesGapMax_FLAG = "--alignMatesGapMax"
        alignMatesGapMax_ARG = 1000000
    
        outSAMunmapped_FLAG = "--outSAMunmapped"
        outSAMunmapped_ARG = "Within"
    
        outFilterType_FLAG = "--outFilterType"
        outFilterType_ARG = "BySJout"
    
        outSAMattributes_FLAG = "--outSAMattributes"
        outSAMattributes_ARG = ['NH', 'HI', 'AS', 'NM', 'MD']
    
        sjdbScore_FLAG = "--sjdbScore"
        sjdbScore_ARG = 1
    
        twopassMode_FLAG = "--twopassMode"
        twopassMode_ARG = "Basic"
    
        twopass1readsN_FLAG = "--twopass1readsN"
        twopass1readsN_ARG = -1
    
        outFileNamePrefix_FLAG = "--outFileNamePrefix"
        outFileNamePrefix_ARG = None
    
        STAR_COMMAND_DICT = OrderedDict([(genomeDir_FLAG, genomeDir_ARG),
                                         (readFilesIn_FLAG, readFilesIn_ARG),
                                         (readFilesCommand_FLAG, readFilesCommand_ARG),
                                         (runThreadN_FLAG, runThreadN_ARG),
                                         (genomeLoad_FLAG, genomeLoad_ARG),
                                         (outFilterMultimapNmax_FLAG, outFilterMultimapNmax_ARG),
                                         (alignSJDBoverhangMin_FLAG, alignSJDBoverhangMin_ARG),
                                         (outFilterMismatchNmax_FLAG, outFilterMismatchNmax_ARG),
                                         (outFilterMismatchNoverReadLmax_FLAG, outFilterMismatchNoverReadLmax_ARG),
                                         (alignIntronMin_FLAG, alignIntronMin_ARG),
                                         (alignIntronMax_FLAG, alignIntronMax_ARG),
                                         (alignMatesGapMax_FLAG, alignMatesGapMax_ARG),
                                         (outSAMunmapped_FLAG, outSAMunmapped_ARG),
                                         (outFilterType_FLAG, outFilterType_ARG),
                                         (outSAMattributes_FLAG, outSAMattributes_ARG),
                                         (sjdbScore_FLAG, sjdbScore_ARG),
                                         (twopassMode_FLAG, twopassMode_ARG),
                                         (twopass1readsN_FLAG, twopass1readsN_ARG),
                                         (outFileNamePrefix_FLAG, outFileNamePrefix_ARG)])