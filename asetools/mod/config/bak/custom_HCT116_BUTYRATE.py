"""
AUTHOR: Matt Durrant

All of the user-customizable options for ASEtools

This is currently configured for the mdurrant account on Stanford's SCG4 cluster.
This file must be correctly configured in order to run the ASEtools pipelines.
"""

from mod.misc.string_constants import *

# Picard execution path and picard version
PICARD_EXECUTION_PATH = "/srv/gs1/software/picard-tools/2.8.0/picard.jar"
PICARD_VERSION = "2.8.0-SNAPSHOT"

# GATK execution path and GATK version
GATK_EXECUTION_PATH = "/srv/gs1/software/gatk/gatk-3.6/GenomeAnalysisTK.jar"
GATK_VERSION = "3.6-0-g89b7209"

# The reference genome fasta to use for all analyses and pipelines.
REFERENCE_GENOME_FASTA = "/srv/gsfs0/projects/bhatt/mdurrant/BUTYRATE_brayon/references/hg19/ucsc.hg19.fasta"

# A dbsnp vcf (you can retrieve this from the GATK bundle)
DBSNP_VCF = "/home/mdurrant/montgomery/mdurrant/data/dbsnp_138.hg19.vcf.gz"

# A bed file of all of the exons found in the genome, for RNAseq variant calling.
GENCODE_EXONS_BED = "/home/mdurrant/montgomery/mdurrant/data/gencode.exons.merged.bed"

# The maximum memory available to java for the process. 50g = 50 gigabytes.
MAX_JAVA_MEMORY = "50g"

# You must specify a python interpreter that will run in a python environment that has been configured to run WASP.
WASP_PYTHON_PATH = "/home/mdurrant/miniconda3/envs/venv2.7/bin/python"


class StarAlignCustomConfig:
    """
    The custom arguments for running STAR RNAseq alignment
    """

    def __init__(self):
        # STAR execution path
        self.execution_path = "/home/mdurrant/miniconda3/bin/STAR"

        # STAR version, recommended is STAR_2.5.2b
        self.version = "STAR_2.5.2b"
        self.version_flag = "--version"

        # Arguments to be passed to star.
        # You can add or remove arguments, but be sure to keep them as tuples.
        # If only single argument, write it as ("--arg","")
        self.args = [

            ("--genomeDir", "/srv/gsfs0/projects/bhatt/mdurrant/BUTYRATE_brayon/references/starGenomeUCSChg19"),
            ("--readFilesCommand", "zcat"),
            ("--runThreadN", 6),
            ("--genomeLoad", "NoSharedMemory"),
            ("--outFilterMultimapNmax", 20),
            ("--alignSJoverhangMin", 8),
            ("--alignSJDBoverhangMin", 1),
            ("--outFilterMismatchNmax", 999),
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


class JavaCustomConfig:
    """
    Configure your java, does not actually execute anything other than self.check_version()
    """

    def __init__(self):
        self.execution_path = "/srv/gs1/software/java/jre1.8.0_66/bin/java"

        # Recommended java version ois 1.8.0_66
        self.version = "1.8.0_66"
        self.version_flag = "-version"

        self.args = None


class PicardAddReadGroupsCustomConfig:
    """
    Configure picard.jar AddOrReplaceReadGroups to run properly.
    """

    def __init__(self):
        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-Xmx%s" % MAX_JAVA_MEMORY,
                                          "-jar",
                                          PICARD_EXECUTION_PATH,
                                          "AddOrReplaceReadGroups"])

        self.version = PICARD_VERSION
        self.version_flag = "--help"

        # You can add or remove arguments, but be sure to keep them as tuples.
        # If only single argument, write it as ("--arg","")
        self.args = [

            ("SO", "coordinate"),
            ("RGID", "id"),
            ("RGLB", "library"),
            ("RGPL", "ILLUMINA"),
            ("RGPU", "machine"),
            ("RGSM", "sample")

        ]


class PicardMarkDuplicatesCustomConfig:
    """
    Configure picard.jar MarkDuplicates.
    """

    def __init__(self):
        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-Xmx%s" % MAX_JAVA_MEMORY,
                                          "-jar",
                                          PICARD_EXECUTION_PATH,
                                          "MarkDuplicates"])

        self.version = PICARD_VERSION
        self.version_flag = "--help"

        # You can add or remove arguments, but be sure to keep them as tuples.
        # If only single argument, write it as ("--arg","")
        self.args = [

            ("CREATE_INDEX", "true"),
            ("VALIDATION_STRINGENCY", "SILENT"),
            ("M", "output.metrics")

        ]


class GATKSplitNCigarReadsCustomConfig:
    """
    Configure GATK SplitNCigarReads
    """

    def __init__(self):
        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-Xmx%s" % MAX_JAVA_MEMORY,
                                          "-jar",
                                          GATK_EXECUTION_PATH,
                                          "-T SplitNCigarReads"])

        self.version = GATK_VERSION
        self.version_flag = "--version"

        # You can add or remove arguments, but be sure to keep them as tuples.
        # If only single argument, write it as ("--arg","")
        self.args = [

            ("-R", REFERENCE_GENOME_FASTA),
            ("-rf", "ReassignOneMappingQuality"),
            ("-RMQF", 255),
            ("-RMQT", 60),
            ("-U", "ALLOW_N_CIGAR_READS")

        ]


class GATKRNAseqBaseRecalibratorCustomConfig:
    """
    Configure GATK BaseRecalibrator.
    """

    def __init__(self):
        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-Xmx%s" % MAX_JAVA_MEMORY,
                                          "-jar",
                                          GATK_EXECUTION_PATH,
                                          "-T BaseRecalibrator"])

        self.version = GATK_VERSION
        self.version_flag = "--version"

        # You can add or remove arguments, but be sure to keep them as tuples.
        # If only single argument, write it as ("--arg","")
        self.args = [

            ("-R", REFERENCE_GENOME_FASTA),
            ("-knownSites", DBSNP_VCF),
            ("-L", GENCODE_EXONS_BED)

        ]


class GATKPrintReadsCustomConfig:
    """
    Configure GATK PrintReads.
    """

    def __init__(self):
        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-Xmx%s" % MAX_JAVA_MEMORY,
                                          "-jar",
                                          GATK_EXECUTION_PATH,
                                          "-T PrintReads"])

        self.version = GATK_VERSION
        self.version_flag = "--version"

        # You can add or remove arguments, but be sure to keep them as tuples.
        # If only single argument, write it as ("--arg","")
        self.args = [

            ("-R", REFERENCE_GENOME_FASTA)

        ]


class GATKHaplotypeCallerCustomConfig:
    """
    Configure GATK HaplotypeCaller
    """

    def __init__(self):
        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-Xmx%s" % MAX_JAVA_MEMORY,
                                          "-jar",
                                          GATK_EXECUTION_PATH,
                                          "-T HaplotypeCaller"])

        self.version = GATK_VERSION
        self.version_flag = "--version"

        # You can add or remove arguments, but be sure to keep them as tuples.
        # If only single argument, write it as ("--arg","")
        self.args = [

            ("-R", REFERENCE_GENOME_FASTA),
            ("-dontUseSoftClippedBases", ""),
            ("-stand_call_conf", 20.0)

        ]


class WASPFindIntersectingSnpsCustomConfig:
    """
    Configure WASP find_intersecting_snps.py
    """

    def __init__(self):
        # You must set up a WASP python environment as described by their docs
        # You then need to call the python interpreter corresponding to that python environment.
        self.execution_path = SPACE.join([WASP_PYTHON_PATH,
                                          "/home/mdurrant/montgomery/mdurrant/ASETools/WASP/mapping/"
                                          "find_intersecting_snps.py"])

        # No version of wasp is necessary.
        self.version = None
        self.version_flag = None

        # You can add or remove arguments, but be sure to keep them as tuples.
        # If only single argument, write it as ("--arg","")
        self.args = [

            ("--is_paired_end", ""),
            ("--is_sorted", ""),

        ]


class WASPFilterRemappedReadsCustomConfig:
    """
    Configure WASP filter_remapped_reads.py
    """

    def __init__(self):
        self.execution_path = SPACE.join([WASP_PYTHON_PATH,
                                          "/home/mdurrant/montgomery/mdurrant/ASETools/WASP/mapping/"
                                          "filter_remapped_reads.py"])

        self.version = None
        self.version_flag = None

        # You can add or remove arguments, but be sure to keep them as tuples.
        # If only single argument, write it as ("--arg","")
        self.args = []


class SamtoolsCustomConfig:
    """
    Configure samtools
    """

    def __init__(self):
        self.execution_path = "/home/mdurrant/miniconda3/envs/venv3.5/bin/samtools"

        # Samtools version 1.3.1 recommended
        self.version = "1.3.1"
        self.version_flag = "--version"

        # You can add or remove arguments, but be sure to keep them as tuples.
        # If only single argument, write it as ("--arg","")
        self.args = None


class SamtoolsMergeCustomConfig:
    """
    Configure samtools merge
    """

    def __init__(self):
        self.execution_path = SPACE.join([SamtoolsCustomConfig().execution_path,
                                          "merge"])

        self.version = None
        self.version_flag = None

        # You can add or remove arguments, but be sure to keep them as tuples.
        # If only single argument, write it as ("--arg","")
        self.args = [
            ('-f', '')
        ]


class SamtoolsSortCustomConfig:
    """
    configure samtools sort
    """

    def __init__(self):
        self.execution_path = SPACE.join([SamtoolsCustomConfig().execution_path,
                                          "sort"])

        self.version = None
        self.version_flag = None

        # You can add or remove arguments, but be sure to keep them as tuples.
        # If only single argument, write it as ("--arg","")
        self.args = []


class SamtoolsIndexCustomConfig:
    """
    Configure samtools index
    """

    def __init__(self):
        self.execution_path = SPACE.join([SamtoolsCustomConfig().execution_path,
                                          "index"])

        self.version = None
        self.version_flag = None

        # You can add or remove arguments, but be sure to keep them as tuples.
        # If only single argument, write it as ("--arg","")
        self.args = []


class GATKVariantFiltrationCustomConfig:
    """
    Configure GATK VariantFiltration
    """

    def __init__(self):
        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-Xmx%s" % MAX_JAVA_MEMORY,
                                          "-jar",
                                          GATK_EXECUTION_PATH,
                                          "-T VariantFiltration"])

        self.version = GATK_VERSION
        self.version_flag = "--version"

        # You can add or remove arguments, but be sure to keep them as tuples.
        # If only single argument, write it as ("--arg","")
        self.args = [

            ("-R", REFERENCE_GENOME_FASTA),
            ("-window", 35),
            ("-cluster", 3),
            ("-filterName", "FS"),
            ("-filter", '\"FS > 30.0\"'),
            ("-filterName", "QD"),
            ("-filter", '\"QD < 2.0\"')

        ]


class GATKASEReadCounterCustomConfig:
    """
    Configure GATK ASEReadCounter
    """

    def __init__(self):
        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-Xmx%s" % MAX_JAVA_MEMORY,
                                          "-jar",
                                          GATK_EXECUTION_PATH,
                                          "-T ASEReadCounter"])

        self.version = GATK_VERSION
        self.version_flag = "--version"

        # You can add or remove arguments, but be sure to keep them as tuples.
        # If only single argument, write it as ("--arg","")
        self.args = [

            ("-R", REFERENCE_GENOME_FASTA),
            ("-U", "ALLOW_N_CIGAR_READS"),
            ("-minDepth", -1),
            ("--minBaseQuality", -1),
            ("--minMappingQuality", -1)

        ]
