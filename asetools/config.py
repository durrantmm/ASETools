#!/usr/bin/env python3
from collections import OrderedDict
import os

class Config:
    # Miscellaneous, change at your own riske
    utf8 = "UTF8"
    empty_string = ''
    config_suffix = '.config'

    # General reference genome in fasta format. For example, ucsc.hg19.fasta
    REFERENCE_GENOME_PATH = "/srv/gsfs0/projects/bhatt/mdurrant/BUTYRATE_brayon/references/hg19/ucsc.hg19.fasta"


    class PipelineFlow:
        global Config

        # Output dir, usually specified as a command line argument.
        MAIN_OUTPUT_DIR = None

        def update_main_path(self, path):
            PipelineFlow.MAIN_OUTPUT_DIR = os.path.abspath(path)

            # Update CallVariantsRNASeq Paths
            PipelineFlow.CallVariantsRNASeq.OUTPUT_DIR = os.path.join(
                PipelineFlow.MAIN_OUTPUT_DIR,
                os.path.basename(PipelineFlow.CallVariantsRNASeq.OUTPUT_DIR))

            PipelineFlow.CallVariantsRNASeq.STAR_ALIGN_READS_CONFIG_PATH = os.path.join(
                PipelineFlow.MAIN_OUTPUT_DIR,
                PipelineFlow.CallVariantsRNASeq.STAR_ALIGN_READS_CONFIG_PATH
            )

            PipelineFlow.CallVariantsRNASeq.PICARD_ADD_OR_REPLACE_READ_GROUPS_CONFIG_PATH = os.path.join(
                PipelineFlow.MAIN_OUTPUT_DIR,
                PipelineFlow.CallVariantsRNASeq.PICARD_ADD_OR_REPLACE_READ_GROUPS_CONFIG_PATH
            )

            PipelineFlow.CallVariantsRNASeq.PICARD_MARK_DUPLICATES_CONFIG_PATH = os.path.join(
                PipelineFlow.MAIN_OUTPUT_DIR,
                PipelineFlow.CallVariantsRNASeq.PICARD_MARK_DUPLICATES_CONFIG_PATH
            )



        class CallVariantsRNASeq:
            global Config
            global PipelineFlow

            OUTPUT_DIR = "call_variants_rna"

            STAR_ALIGN_READS = "align_reads"
            PICARD_ADD_OR_REPLACE_READ_GROUPS = "add_read_groups"
            PICARD_MARK_DUPLICATES = "mark_duplicates"

            ORDER = [STAR_ALIGN_READS, PICARD_ADD_OR_REPLACE_READ_GROUPS, PICARD_MARK_DUPLICATES]
            START = STAR_ALIGN_READS

            STAR_ALIGN_READS_CONFIG_PATH = Config.empty_string.join([STAR_ALIGN_READS, Config.config_suffix])
            PICARD_ADD_OR_REPLACE_READ_GROUPS_CONFIG_PATH = Config.empty_string.join([PICARD_ADD_OR_REPLACE_READ_GROUPS, Config.config_suffix])
            PICARD_MARK_DUPLICATES_CONFIG_PATH = Config.empty_string.join([PICARD_MARK_DUPLICATES, Config.config_suffix])



    class Java:
        PATH = "/srv/gs1/software/java/jre1.8.0_66/bin/java"
        VERSION = "1.8.0_66"
        VERSION_FLAG = "-version"
        PARSE_VERSION = lambda x: x
        VERSION_ERROR = "Your java is version {ACTUAL}, not {EXPECTED}, as specified in the config file."


    class STAR:
        global utf8

        # Path to the star aligner, absolute path is preferred over aliases
        PATH = "/home/mdurrant/miniconda3/bin/STAR"
        # The version of STAR aligner. Change at your own risk.
        # These are the options for the STAR alignment command
        # If the argument is optional, set its value to None to exclude.
        VERSION = "STAR_2.5.2b"
        VERSION_FLAG = '--version'
        PARSE_VERSION = lambda x: x.decode(utf8)
        VERSION_ERROR = "The STAR aligner is version {ACTUAL}, not {EXPECTED}, as specified in the config file."

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

    class Picard:

        PATH = "/srv/gs1/software/picard-tools/2.8.0/picard.jar"


        class AddOrReplaceReadGroups:

            INPUT_FLAG = "I="
            INPUT_ARG = None

            OUTPUT_FLAG = "O="
            OUTPUT_ARG = None

            SORT_ORDER_FLAG = "SO="
            SORT_ORDER_ARG = "coordinate"

            RGID_FLAG = "RGID="
            RGID_ARG = "id"

            RGLB_FLAG = "RGLB="
            RGLB_ARG = "library"

            RGPL_FLAG = "RGPL="
            RGPL_ARG = "platform"

            RGPU_FLAG = "RGPU="
            RGPU_ARG = "machine"

            RGSM_FLAG = "RGSM="
            RGSM_ARG = "sample"

        class MarkDuplicates:
            java - jar
            picard.jar
            MarkDuplicates
            I = rg_added_sorted.bam
            O = dedupped.bam
            CREATE_INDEX = true
            VALIDATION_STRINGENCY = SILENT
            M = output.metrics

