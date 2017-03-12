import sys
from collections import defaultdict

rnaseq_filter = "RNASEQ_FILTER"	
rnaseq_het = "RNASEQ_HET"
atacseq_filter = "ATACSEQ_FILTER"
atacseq_het = "ATACSEQ_HET"
genchip_het = "GENOTYPE_CHIP_HET"	
exome_het = "EXOME_VARIANT_HET"
in1000g = "IN_1000G"

exome_gt_key = "EXOME_GT"
genchip_gt_key = "GENOTYPE_CHIP_GT"
rnavar_het_key = "RNA_VAR_HET"
atacvar_het_key = "ATAC_VAR_HET"
stringent_key = 'STRINGENT'
moderate_key = "MODERATE"
lenient_key = "LENIENT"
rnaseq_filter_stringent_key = "RNASEQ_FILTER_STRINGENT_GT"
rnaseq_filter_moderate_key = "RNASEQ_FILTER_MODERATE_GT"
rnaseq_filter_lenient_key = "RNASEQ_FILTER_LENIENT_GT"
none_key = "NONE"
atacseq_filter_lenient_key = "ATACSEQ_GT_LENIENT"
atacseq_filter_stringent_key = "ATACSEQ_GT_STRINGENT"

equals_key = '=='
not_equals_key = '!='

het_key = 'HET'
true_key = 'TRUE'
false_key = 'FALSE'

def run(bool_path, table_path):

	bool_keys = parse_bools_to_functions(bool_path)
	table = parse_table(table_path)

	bool_key_matches = defaultdict(int)

	i = 0
	j = 0
	for bool in bool_keys:
		i += 1

		for line in table:
			j += 1

			if j % 1000000 == 0:
				print(i, j)

			if passes_bool(line, bool):
				bool_key_matches[i] += 1

	for i in range(len(bool_keys)):
		if i in bool_key_matches:
			print('\t'.join(map(str, [i, bool_key_matches[i]])))



def parse_bools_to_functions(bool_path):

	global rnaseq_filter, rnaseq_het, atacseq_filter, atacseq_het, genchip_het, exome_het, in1000g, \
		exome_gt_key, equals_key, not_equals_key, het_key, true_key, false_key, genchip_gt_key, rnavar_het_key, \
		rnaseq_filter_stringent_key, rnaseq_filter_moderate_key, rnaseq_filter_lenient_key, atacvar_het_key, \
		stringent_key, moderate_key, lenient_key, none_key, atacseq_filter_lenient_key, atacseq_filter_stringent_key

	all_bool_keys = []

	with open(bool_path) as infile:

		header = infile.readline().strip().split()

		for line in infile:
			bool_keys = []

			line = line.strip().split()
			line = {header[i]:line[i] for i in range(len(line))}
			if line[exome_het] == true_key:
				bool_keys.append((exome_gt_key, equals_key, het_key))
			elif line[exome_het] == false_key:
				bool_keys.append((exome_gt_key, not_equals_key, het_key))

			if line[genchip_het] == true_key:
				bool_keys.append((genchip_gt_key, equals_key, het_key))
			elif line[genchip_het] == false_key:
				bool_keys.append((genchip_gt_key, not_equals_key, het_key))

			if line[rnaseq_het] == true_key:
				bool_keys.append((rnavar_het_key, equals_key, true_key))
			elif line[rnaseq_het] == false_key:
				bool_keys.append((rnavar_het_key, not_equals_key, true_key))

			if line[atacseq_het] == true_key:
				bool_keys.append((atacvar_het_key, equals_key, true_key))
			elif line[atacseq_het] == false_key:
				bool_keys.append((atacvar_het_key, not_equals_key, true_key))

			if line[rnaseq_filter] == stringent_key:
				bool_keys.append((rnaseq_filter_stringent_key, not_equals_key, none_key))
			elif line[rnaseq_filter] == moderate_key:
				bool_keys.append((rnaseq_filter_moderate_key, not_equals_key, none_key))
			elif line[rnaseq_filter] == lenient_key:
				bool_keys.append((rnaseq_filter_lenient_key, not_equals_key, none_key))

			if line[in1000g] == true_key:
				bool_keys.append((in1000g, equals_key, true_key))
			elif line[in1000g] == false_key:
				bool_keys.append((in1000g, equals_key, false_key))

			if line[atacseq_filter] == lenient_key:
				bool_keys.append((atacseq_filter_lenient_key, not_equals_key, none_key))
			elif line[atacseq_filter] == stringent_key:
				bool_keys.append((atacseq_filter_stringent_key, not_equals_key, none_key))

			all_bool_keys.append(bool_keys)

	return all_bool_keys

def parse_table(table_path):
	outtable = []
	with open(table_path) as infile:
		header = infile.readline().strip().split()
		for line in infile:
			line = line.strip().split()
			line = {header[i]:line[i] for i in range(len(line))}
			outtable.append(line)

	return outtable

def passes_bool(line, boolean_keys):
	for key in boolean_keys:
		if key[1] == '==':
			if line[key[0]] != key[2]:
				return False

		elif key[1] == '!=':
			if line[key[0]] == key[2]:
				return False
		else:
			print("WEIRD")

	return True


if __name__ == "__main__":
	bool_path = sys.argv[1]
	table_path = sys.argv[2]

	run(bool_path, table_path)
		
		
