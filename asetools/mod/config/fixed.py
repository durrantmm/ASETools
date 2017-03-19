"""
AUTHOR: Matt Durrant

This is a companion module to the custom.py module.

These are the configurations that the user should not touch - they are fixed and independent of the user's environment.
"""

from mod.misc.record_classes import FlagTwoArgs, FlagArg
from mod.misc.version_parsers import *


class StarAlignFixedConfig:
    def __init__(self):
        self.name = "STAR"

        self.input_file = FlagTwoArgs(flag='--readFilesIn', arg1=None, arg2=None)

        self.output_file = FlagArg(flag='--outFileNamePrefix', arg=None)

        self.version_parser = parse_star_version

        self.log_name = "star_align.json"


class JavaFixedConfig:
    def __init__(self):
        self.name = "Java"

        self.input_file = None

        self.output_file = None

        self.version_parser = parse_java_version

        self.log_name = None


class PicardAddReadGroupsFixedConfig:
    def __init__(self):
        self.name = "AddOrReplaceReadGroups"

        self.input_file = FlagArg(flag='I', arg=None)

        self.output_file = FlagArg(flag='O', arg=None)

        self.version_parser = parse_add_read_groups_version

        self.log_name = "add_read_groups.json"


class PicardMarkDuplicatesFixedConfig:
    def __init__(self):
        self.name = "MarkDuplicates"

        self.input_file = FlagArg(flag='I', arg=None)

        self.output_file = FlagArg(flag='O', arg=None)

        self.version_parser = parse_mark_duplicates_version

        self.log_name = "mark_duplicates.json"


class GATKSplitNCigarReadsFixedConfig:
    def __init__(self):
        self.name = "GATK-SplitNCigarReads"

        self.input_file = FlagArg(flag='-I', arg=None)

        self.output_file = FlagArg(flag='-o', arg=None)

        self.version_parser = parse_gatk_version

        self.log_name = "split_n_cigar_reads.json"


class GATKRNAseqBaseRecalibratorFixedConfig:
    def __init__(self):
        self.name = "GATK-BaseRecalibrator"

        self.input_file = FlagArg(flag='-I', arg=None)

        self.output_file = FlagArg(flag='-o', arg="recal.table")

        self.version_parser = parse_gatk_version

        self.log_name = "base_recalibrator.json"


class GATKPrintReadsFixedConfig:
    def __init__(self):
        self.name = "GATK-PrintReads"

        self.input_file = FlagArg(flag='-I', arg=None)

        self.input_recal_table = FlagArg(flag='-BQSR', arg=None)

        self.output_file = FlagArg(flag='-o', arg=None)

        self.version_parser = parse_gatk_version

        self.log_name = "print_reads.json"


class GATKHaplotypeCallerFixedConfig:
    def __init__(self):
        self.name = "GATK-HaplotypeCaller"

        self.input_file = FlagArg(flag='-I', arg=None)

        self.output_file = FlagArg(flag='-o', arg=None)

        self.version_parser = parse_gatk_version

        self.log_name = "haplotype_caller.json"


class GATKVariantFiltrationFixedConfig:
    def __init__(self):
        self.name = "GATK-VariantFiltration"

        self.input_file = FlagArg(flag='-V', arg=None)

        self.output_file = FlagArg(flag='-o', arg=None)

        self.version_parser = parse_gatk_version

        self.log_name = "variant_filtration.json"


class WASPFindIntersectingSnpsFixedConfig:
    def __init__(self):
        self.name = "WASP-FindIntersectingSnps"

        self.input_file = FlagArg(flag='', arg=None)

        self.output_file = FlagArg(flag='--output_dir', arg=None)

        self.version_parser = parse_gatk_version

        self.log_name = "wasp_find_intersecting_snps.json"


class WASPFilterRemappedReadsFixedConfig:
    def __init__(self):
        self.name = "WASP-FilterRemappedReads"

        self.input_file = FlagTwoArgs(flag='', arg1=None, arg2=None)

        self.output_file = FlagArg(flag='', arg=None)

        self.version_parser = parse_gatk_version

        self.log_name = "wasp_filter_remapped_reads.json"


class SamtoolsFixedConfig:
    def __init__(self):
        self.name = "Samtools"

        self.input_file = None

        self.output_file = None

        self.version_parser = parse_samtools_version

        self.log_name = None


class SamtoolsMergeFixedConfig:
    def __init__(self):
        self.name = "Samtools Merge"

        self.input_file = FlagTwoArgs(flag='', arg1=None, arg2=None)

        self.output_file = FlagArg(flag='', arg=None)

        self.version_parser = None

        self.log_name = "samtools_merge.json"


class SamtoolsSortFixedConfig:
    def __init__(self):
        self.name = "Samtools Sort"

        self.input_file = FlagArg(flag='', arg=None)

        self.output_file = FlagArg(flag='-o', arg=None)

        self.version_parser = None

        self.log_name = "samtools_sort_index.json"


class SamtoolsIndexFixedConfig:
    def __init__(self):
        self.name = "Samtools Index"

        self.input_file = FlagArg(flag='', arg=None)

        self.output_file = FlagArg(flag='', arg=None)

        self.version_parser = None

        self.log_name = "samtools_index.json"


class GATKASEReadCounterFixedConfig:
    def __init__(self):
        self.name = "GATK-ASEReadCounter"

        self.input_file = FlagArg(flag='-I', arg=None)

        self.input_sites = FlagArg(flag='-sites', arg=None)

        self.output_file = FlagArg(flag='-o', arg=None)

        self.version_parser = parse_gatk_version

        self.log_name = "ase_read_counter.json"


class RNASeqVariantCallingFixedConfig:
    def __init__(self):
        self.name = "RNAseqVariantCaller"

        self.input_file = FlagTwoArgs(flag='--readFilesIn', arg1=None, arg2=None)


class WASPAlleleSpecificExpressionPipelineFixedConfig:
    def __init__(self):
        self.name = "WASP-ASE-subprocess"

        self.input_file = FlagTwoArgs(flag='--readFilesIn', arg1=None, arg2=None)
