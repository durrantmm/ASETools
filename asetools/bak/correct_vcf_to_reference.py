import sys
import vcf
import gzip
from Bio import SeqIO
from collections import defaultdict

reference_format = "fasta"
vcf_header_start = "#CHROM"

def correct_vcf(vcf_path, snp_reference_path, reference_path):
    global reference_format
    out_vcf_path = vcf_path.split('.')[0] + '.CORRECTED.vcf'

    reference = SeqIO.parse(reference_path, reference_format)
    current_chrom = next(reference)

    vcf_reader = vcf.Reader(filename=vcf_path)
    vcf_writer = vcf.Writer(open(out_vcf_path, 'w'), vcf_reader)

    #ref_snp_dict = get_ref_snp_dicts(snp_reference_path)

    for var in vcf_reader:
        if len(var.ALT) > 1:
            raise TypeError("The vcf has multi-allelic sites. NOT COOL.")

        current_chrom = get_chrom(current_chrom, reference, var.CHROM)
        query_info = [var.CHROM, var.POS, var.ID, var.REF, str(var.ALT[0])]
        true_ref = get_true_ref(current_chrom, var.POS)

        adjust_variant_record_simple(var, query_info, true_ref)
        #var = adjust_variant_record(var, query_info, true_ref, ref_snp_dict)
        #print(var)

def adjust_variant_record_simple(variant_rec, query_info, true_ref):
    query_chrom, query_pos, query_id, query_ref, query_alt = query_info

    if query_ref == true_ref:
        GT = variant_rec.samples[0]['GT']
        print(output_line(query_chrom, query_pos, query_id, query_ref, query_alt, GT, GT))

    elif query_alt == true_ref:
        GT = variant_rec.samples[0]['GT']
        print(output_line(query_chrom, query_pos, query_id, query_alt, query_ref, flip_genotype(GT), GT))

    elif query_ref == complement_base(true_ref):
        query_ref = complement_base(query_ref)
        query_alt = complement_base(query_alt)
        GT = variant_rec.samples[0]['GT']
        print(output_line(query_chrom, query_pos, query_id, query_ref, query_alt, GT, GT))

    elif query_alt == complement_base(true_ref):
        query_ref = complement_base(query_ref)
        query_alt = complement_base(query_alt)
        GT = variant_rec.samples[0]['GT']
        print(output_line(query_chrom, query_pos, query_id, query_alt, query_ref, flip_genotype(GT), GT))

    else:
        print("UNEXPECTED")
        print(query_info, true_ref)
        sys.exit()


def adjust_variant_record(variant_rec, query_info, true_ref, ref_snp_dict):

    query_chrom, query_pos, query_id, query_ref, query_alt = query_info

    if reference_contains_id_and_location(query_chrom, query_pos, query_id, ref_snp_dict):

        return TRUE_reference_contains_id_and_location(variant_rec, query_info, true_ref, ref_snp_dict)

    else:

        return FALSE_reference_contains_id_and_location(variant_rec, query_info, true_ref, ref_snp_dict)


def reference_contains_id_and_location(query_chrom, query_pos, query_id, ref_snp_dict):
    loc_key = (query_chrom, query_pos)

    if loc_key in ref_snp_dict.keys() and query_id in ref_snp_dict.keys():

        if len(ref_snp_dict[loc_key]) > 1 or len(ref_snp_dict[query_id]) > 1:
            print(query_chrom, query_pos, query_id, ref_snp_dict[loc_key], ref_snp_dict[query_id])
            raise TypeError("There are multiple position matches. Might want to handle this.")
        else:
            return True

    else:
        return False


def TRUE_reference_contains_id_and_location(variant_rec, query_info, true_ref, ref_snp_dict):
    query_chrom, query_pos, query_id, query_ref, query_alt = query_info
    query_loc = (query_chrom, query_pos)

    comp_info_rsid = ref_snp_dict[query_id][0]
    comp_info_loc = ref_snp_dict[query_loc][0]

    if comparison_variants_are_equal(comp_info_rsid, comp_info_loc):

        TRUE_comparison_variants_are_equal(variant_rec, query_info, comp_info_rsid, true_ref)

    else:

        FALSE_comparison_variants_are_equal(variant_rec, query_info, comp_info_rsid, comp_info_loc, true_ref)

def FALSE_reference_contains_id_and_location(variant_rec, query_info, true_ref, ref_snp_dict):
    query_chrom, query_pos, query_id, query_ref, query_alt = query_info
    print("ALLELES NOT IN REFERENCE")
    if query_ref == true_ref:
        print("CORRECT ORDER AND ORIENTATION")
        GT = variant_rec.samples[0]['GT']
        print(query_info, true_ref)
        print(output_line(query_chrom, query_pos, query_id, query_ref, query_alt, GT))

    elif query_ref == complement_base(true_ref):
        print("CORRECT ORDER, INCORRECT ORIENTATION")
        query_ref = complement_base(query_ref)
        query_alt = complement_base(query_alt)
        GT = variant_rec.samples[0]['GT']
        print(query_info, true_ref)
        print(output_line(query_chrom, query_pos, query_id, query_ref, query_alt, GT))

    elif query_alt == true_ref:
        print("INCORRECT ORDER, CORRECT ORIENTATION")
        GT = variant_rec.samples[0]['GT']
        print(query_info, true_ref)
        print(output_line(query_chrom, query_pos, query_id, query_alt, query_ref, flip_genotype(GT)))

    elif query_alt == complement_base(true_ref):
        print("INCORRECT ORDER, INCORRECT ORIENTATION")
        query_ref = complement_base(query_ref)
        query_alt = complement_base(query_alt)
        GT = variant_rec.samples[0]['GT']
        print(query_info, true_ref)
        print(output_line(query_chrom, query_pos, query_id, query_alt, query_ref, flip_genotype(GT)))

def TRUE_comparison_variants_are_equal(variant_rec, query_info, comp_info, true_ref):
    query_chrom, query_pos, query_id, query_ref, query_alt = query_info
    comp_chrom, comp_pos, comp_id, comp_ref, comp_alleles = comp_info

    if alleles_match(query_ref, query_alt, comp_alleles):
        print("ALLELES MATCH")
        if query_ref == true_ref:
            print("CORRECT ORDER")
            GT = variant_rec.samples[0]['GT']
            print(query_info, comp_info, true_ref)
            print(output_line(query_chrom, query_pos, query_id, query_ref, query_alt, GT))

        elif query_alt == true_ref:
            print("INCORRECT ORDER")
            GT = variant_rec.samples[0]['GT']
            print(query_info, comp_info, true_ref)
            print(output_line(query_chrom, query_pos, query_id, query_alt, query_ref, flip_genotype(GT)))

    elif alleles_match_complement(query_ref, query_alt, comp_alleles):
        print("ALLELES MATCH COMPLEMENT")
        if query_ref == true_ref:
            print("CORRECT ORDER AND ORIENTATION")
            GT = variant_rec.samples[0]['GT']
            print(query_info, comp_info, true_ref)
            print(output_line(query_chrom, query_pos, query_id, query_ref, query_alt, GT))

        elif query_ref == complement_base(true_ref):
            print("CORRECT ORDER, INCORRECT ORIENTATION")
            query_ref = complement_base(query_ref)
            query_alt = complement_base(query_alt)
            GT = variant_rec.samples[0]['GT']
            print(query_info, comp_info, true_ref)
            print(output_line(query_chrom, query_pos, query_id, query_ref, query_alt, GT))

        elif query_alt == true_ref:
            print("INCORRECT ORDER, CORRECT ORIENTATION")
            GT = variant_rec.samples[0]['GT']
            print(query_info, comp_info, true_ref)
            print(output_line(query_chrom, query_pos, query_id, query_alt, query_ref, flip_genotype(GT)))

        elif query_alt == complement_base(true_ref):
            print("INCORRECT ORDER, INCORRECT ORIENTATION")
            query_ref = complement_base(query_ref)
            query_alt = complement_base(query_alt)
            GT = variant_rec.samples[0]['GT']
            print(query_info, comp_info, true_ref)
            print(output_line(query_chrom, query_pos, query_id, query_alt, query_ref, flip_genotype(GT)))

        print(query_info, comp_info, true_ref)

    else:
        print(query_info, comp_info, true_ref)
        sys.exit()


def FALSE_comparison_variants_are_equal(variant_rec, query_info, comp_info_rsid, comp_info_loc, true_ref):
    print('variant_rec:', variant_rec)
    print('query_info:', query_info)
    print('comp_info_rsid:', comp_info_rsid)
    print('comp_info_loc:', comp_info_loc)
    print('true_ref:', true_ref)
    raise TypeError('COMPARISON VARIANTS ARE NOT EQUAL!!!!')



def comparison_variants_are_equal(comp_info_rsid, comp_info_loc):
    if comp_info_rsid == comp_info_loc:
        return True
    else:
        return False


def alleles_match(ref1, alt1, alleles):
    if ref1 in alleles and alt1 in alleles:
        return True
    else:
        return False

def alleles_match_complement(ref1, alt1, alleles):
    if complement_base(ref1) in alleles and complement_base(alt1) in alleles:
        return True
    else:
        return False

def positions_match(chrom1, pos1, chrom2, pos2):
    if chrom1 == chrom2 and pos1 == pos2:
        return True
    else:
        return False

def complement_base(base):
    if base == 'A':
        return 'T'
    elif base == 'T':
        return 'A'
    elif base == 'C':
        return 'G'
    elif base == 'G':
        return 'C'
    else:
        return base

def interpret_genotype(gt):
    if gt in ['0/1', '1/0']:
        return "HET"
    elif gt == '1/1':
        return "HOM_ALT"
    elif gt == '0/0':
        return "HOM_REF"

def flip_genotype(gt):
    if gt == '1/1':
        return '0/0'
    elif gt == '0/0':
        return '1/1'
    else:
        return gt

def output_line(query_chrom, query_pos, query_id, query_ref, query_alt, gt, gt_orig):
    gt, gt_orig = interpret_genotype(gt), interpret_genotype(gt_orig)
    return '\t'.join(map(str, [query_chrom, query_pos, query_ref, query_alt, query_id, gt]))

def get_ref_snp_dicts(path):
    snp_dict = defaultdict(list)

    with open(path) as infile:
        for line in infile:
            line = line.strip().split()
            chrom, pos, id, ref, alleles, strand = [line[0], int(line[1]), line[2], line[4], set(line[5].split('/')),
                                                    line[3]]
            if strand == '+':
                snp_dict[id].append([chrom, pos, id, ref, alleles])
                snp_dict[(chrom, pos)].append([chrom, pos, id, ref, alleles])
            elif strand == '-':
                alleles = set([complement_base(base) for base in alleles])
                ref = complement_base(ref)
                snp_dict[id].append([chrom, pos, id, ref, alleles])
                snp_dict[(chrom, pos)].append([chrom, pos, id, ref, alleles])
            else:
                print("WEIRD")
                sys.exit()

    return dict(snp_dict)



def get_chrom(current_chrom, reference, selected_chrom):
    if str(current_chrom.id) == str(selected_chrom):
        return current_chrom
    else:
        while str(current_chrom.id) != str(selected_chrom):
            current_chrom = next(reference)
        return current_chrom

def get_true_ref(current_chrom, pos):
    return current_chrom.seq[pos-1].upper()






if __name__ == '__main__':
    vcf_path = sys.argv[1]
    snp_reference_path = sys.argv[2]
    genome_reference_path = sys.argv[3]

    correct_vcf(vcf_path, snp_reference_path, genome_reference_path)
