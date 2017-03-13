import sys
from mod.misc.string_constants import *


PICARD_EXECUTION_PATH = "/srv/gs1/software/picard-tools/2.8.0/picard.jar"
PICARD_VERSION = "2.8.0-SNAPSHOT"

GATK_EXECUTION_PATH = "/srv/gs1/software/gatk/gatk-3.6/GenomeAnalysisTK.jar"
GATK_VERSION = "3.6-0-g89b7209"

REFERENCE_GENOME_FASTA = "/srv/gsfs0/projects/bhatt/mdurrant/BUTYRATE_brayon/references/hg19/ucsc.hg19.fasta"

DBSNP_VCF = "/home/mdurrant/montgomery/mdurrant/data/All_20151104.vcf.gz"
EXAC_VCF = "/home/mdurrant/montgomery/mdurrant/data/ExAC.r1.sites.vep.vcf.gz"
THOUSAND_GENOMES_VCF = "/home/mdurrant/montgomery/mdurrant/data/1000G_20130502/" \
                       "ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf.gz"
GENCODE_EXONS_BED = "/home/mdurrant/montgomery/mdurrant/data/gencode.exons.merged.bed"

class StarAlignCustomConfig:

    def __init__(self):

        self.execution_path = "/home/mdurrant/miniconda3/bin/STAR"
        self.version = "STAR_2.5.2b"
        self.version_flag = "--version"

        self.args = [

            ("--genomeDir", "/srv/gsfs0/projects/bhatt/mdurrant/BUTYRATE_brayon/references/starGenomeUCSChg19"),
            ("--readFilesCommand", "zcat"),
            ("--runThreadN", 2),
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

    def __init__(self):

        self.execution_path = "/srv/gs1/software/java/jre1.8.0_66/bin/java"
        self.version = "1.8.0_66"
        self.version_flag = "-version"

        self.args = None


class PicardAddReadGroupsCustomConfig:

    def __init__(self):

        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-jar",
                                          PICARD_EXECUTION_PATH,
                                          "AddOrReplaceReadGroups"])

        self.version = PICARD_VERSION
        self.version_flag = "--help"

        self.args = [

            ("SO", "coordinate"),
            ("RGID", "id"),
            ("RGLB", "library"),
            ("RGPL", "ILLUMINA"),
            ("RGPU", "machine"),
            ("RGSM", "sample")

        ]


class PicardMarkDuplicatesCustomConfig:

    def __init__(self):

        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-jar",
                                          PICARD_EXECUTION_PATH,
                                          "MarkDuplicates"])

        self.version = PICARD_VERSION
        self.version_flag = "--help"

        self.args = [

            ("CREATE_INDEX", "true"),
            ("VALIDATION_STRINGENCY", "SILENT"),
            ("M", "output.metrics")

        ]

class GATKSplitNCigarReadsCustomConfig:

    def __init__(self):
        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-jar",
                                          GATK_EXECUTION_PATH,
                                          "-T SplitNCigarReads"])

        self.version = GATK_VERSION
        self.version_flag = "--version"

        self.args = [

            ("-R", REFERENCE_GENOME_FASTA),
            ("-rf", "ReassignOneMappingQuality"),
            ("-RMQF", 255),
            ("-RMQT", 60),
            ("-U", "ALLOW_N_CIGAR_READS")

        ]


class GATKRNAseqBaseRecalibratorCustomConfig:

    def __init__(self):
        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-jar",
                                          GATK_EXECUTION_PATH,
                                          "-T BaseRecalibrator"])

        self.version = GATK_VERSION
        self.version_flag = "--version"

        self.args = [

            ("-R", REFERENCE_GENOME_FASTA),
            ("-knownSites", DBSNP_VCF),
            ("-knownSites", EXAC_VCF),
            ("-knownSites", THOUSAND_GENOMES_VCF),
            ("-L", GENCODE_EXONS_BED)

        ]

class GATKPrintReadsCustomConfig:

    def __init__(self):
        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-jar",
                                          GATK_EXECUTION_PATH,
                                          "-T PrintReads"])

        self.version = GATK_VERSION
        self.version_flag = "--version"

        self.args = [

            ("-R", REFERENCE_GENOME_FASTA)

        ]

class GATKHaplotypeCallerCustomConfig:

    def __init__(self):
        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-jar",
                                          GATK_EXECUTION_PATH,
                                          "-T HaplotypeCaller"])

        self.version = GATK_VERSION
        self.version_flag = "--version"

        self.args = [

            ("-R", REFERENCE_GENOME_FASTA),
            ("-dontUseSoftClippedBases", ""),
            ("-stand_call_conf", 20.0)

        ]


class GATKVariantFiltrationCustomConfig:

    def __init__(self):
        self.execution_path = SPACE.join([JavaCustomConfig().execution_path,
                                          "-jar",
                                          GATK_EXECUTION_PATH,
                                          "-T VariantFiltration"])

        self.version = GATK_VERSION
        self.version_flag = "--version"

        self.args = [

            ("-R", REFERENCE_GENOME_FASTA),
            ("-window", 35),
            ("-cluster", 3),
            ("-filterName", "FS"),
            ("-filter", '\"FS > 30.0\"'),
            ("-filterName", "QD"),
            ("-filter", '\"QD < 2.0\"')

        ]
