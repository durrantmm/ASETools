import sys
import vcf


def compare_vcfs(query_vcf_path, comparison_vcf_path):

    query_vcf = vcf.Reader(filename=query_vcf_path, compressed=True)
    comparison_vcf = vcf.Reader(filename=comparison_vcf_path, compressed=True)

    get_comparison_stats(query_vcf, comparison_vcf)



def get_comparison_stats(query_vcf, comparison_vcf):
    query_total_vars = 0
    query_equals_comparison = 0
    query_absent_comparison = 0
    query_diff_comparison = 0

    print('\t'.join(['CHROM', 'POS', 'vcf1_REF', 'vcf1_ALT', 'vcf2_REF', 'vcf2_ALT', 'vcf1_ID', 'vcf2_ID', 'TYPE',
                     'hom_ref', 'het', 'hom_alt', 'missing']))
    for query_rec in query_vcf:
        try:
            inc_query_equals_comparison = False
            inc_query_absent_comparison = False
            inc_query_diff_comparison = False

            comparison_vars = comparison_vcf.fetch(query_rec.CHROM, query_rec.POS-1, query_rec.POS)

            comparison_var = list(comparison_vars)

            if len(comparison_var) == 1:

                comp_var = comparison_var[0]

                if [query_rec.CHROM, query_rec.POS] == [comp_var.CHROM, comp_var.POS]:

                    alleles1 = set([query_rec.REF] + [str(al) for al in query_rec.ALT])
                    alleles2 = set([comp_var.REF] + [str(al) for al in comp_var.ALT])

                    if alleles1 == alleles2 or are_complementary(alleles1, alleles2):
                        if len(comp_var.get_hets()) > 0:
                            inc_query_equals_comparison = True
                        else:
                            inc_query_diff_comparison = True

                    else:
                        inc_query_absent_comparison = True

            elif len(comparison_var) == 0:
                comp_var = None
                inc_query_absent_comparison = True

            elif len(comparison_var) > 1:
                print("VCF COMPARISON ERROR")
                sys.exit()

            comp_var_id = 'NA'
            if comp_var:
                if comp_var.ID:
                    comp_var_id = comp_var.ID

            query_rec_id = 'NA'
            if query_rec.ID:
                query_rec_id = query_rec.ID


            genotype_counts = count_genotypes(query_rec)
            if inc_query_absent_comparison:
                query_absent_comparison += 1
                print('\t'.join(map(str, [query_rec.CHROM, query_rec.POS, query_rec.REF, '\t'.join(map(str, query_rec.ALT)), 'NA',
                                 'NA', query_rec_id, 'NA', 'MISSING'] + list(map(str, genotype_counts)))))

            if inc_query_equals_comparison:
                query_equals_comparison +=1
                print('\t'.join(map(str, [query_rec.CHROM, query_rec.POS, query_rec.REF, '\t'.join(map(str, query_rec.ALT)), comp_var.REF,
                                ','.join(map(str, comp_var.ALT)), query_rec_id, comp_var_id, 'MATCHED'] + list(map(str, genotype_counts)))))

            if inc_query_diff_comparison:
                query_diff_comparison += 1
                print('\t'.join(map(str, [query_rec.CHROM, query_rec.POS, query_rec.REF, '\t'.join(map(str, query_rec.ALT)), comp_var.REF,
                                 ','.join(map(str, comp_var.ALT)), query_rec_id, comp_var_id, 'DIFFERENT'] + list(map(str, genotype_counts)))))


        except ValueError:
            continue

    return query_total_vars, query_absent_comparison, query_equals_comparison, query_diff_comparison


def count_genotypes(rec_in):
    genotype_counts = {'hom_ref':0, 'het':0, 'hom_alt':0, 'missing':0}
    hom_ref_forms = ['0/0', '0|0']
    het_forms = ['0/1', '0|1', '1/0', '1|0']
    hom_alt_forms = ['1/1', '1|1']
    for samp in rec_in.samples:
        GT = str(samp['GT'])
        if GT in het_forms:
            genotype_counts['het'] += 1
        elif GT in hom_ref_forms:
            genotype_counts['hom_ref'] += 1
        elif GT in hom_alt_forms:
            genotype_counts['hom_alt'] += 1
        else:
            genotype_counts['missing'] += 1

    genotype_counts = [genotype_counts['hom_ref'], genotype_counts['het'],
                       genotype_counts['hom_alt'], genotype_counts['missing']]
    return genotype_counts


def are_complementary(alleles1, alleles2):
    complementary = True

    if len(alleles1) != len(alleles2):
        complementary = False

    for al in alleles1:
        if get_complement_base(al) not in alleles2:
            complementary = False

    return complementary


def get_complement_base(base):
    if base == 'A':
        return 'T'
    elif base == 'T':
        return 'A'
    elif base == 'C':
        return 'G'
    elif base == 'G':
        return 'C'


if __name__ == '__main__':
    # USAGE: python compare_vcfs.py first_vcf.vcf.gz second_vcf.vcf.gz
    query_vcf = sys.argv[1]
    comparison_vcf = sys.argv[2]




    compare_vcfs(query_vcf, comparison_vcf)