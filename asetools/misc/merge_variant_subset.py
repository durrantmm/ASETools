import sys, vcf


def merge_info(super_set_path, subset_vcf_path, column_name):
    superset_reader = get_superset_reader(super_set_path)
    subset_vcf_reader = get_subset_reader(vcf.Reader(filename=subset_vcf_path))

    header = next(superset_reader)
    header.append(column_name)
    print('\t'.join(header))

    super_chrom, super_pos, super_ref, super_alt, super_snps= next(superset_reader)
    sub_chrom, sub_pos, sub_ref, sub_alt, sub_snp = next(subset_vcf_reader)

    while True:
        try:
            if snp1_less_than_snp2(super_chrom, super_pos, sub_chrom, sub_pos):
                write_super_snps_false(super_snps)
                super_chrom, super_pos, super_ref, super_alt, super_snps = next(superset_reader)

            elif snp1_less_than_snp2(sub_chrom, sub_pos, super_chrom, super_pos):
                sub_chrom, sub_pos, sub_ref, sub_alt, sub_snp = next(subset_vcf_reader)

            elif are_equal(super_chrom, super_pos, super_ref, super_alt, sub_chrom, sub_pos, sub_ref, sub_alt):
                write_super_snps_true(super_snps)

                super_chrom, super_pos, super_ref, super_alt, super_snps = next(superset_reader)
                sub_chrom, sub_pos, sub_ref, sub_alt, sub_snp = next(subset_vcf_reader)

            else:
                print("ERROR")
                sys.exit()

        except StopIteration:
            break

    for super_chrom, super_pos, super_ref, super_alt, super_snps in superset_reader:
        write_super_snps_false(super_snps)



def write_super_snps_false(snps):
    for snp in snps:
        snp_out = snp
        snp_out.append(str(False))
        print('\t'.join(snp_out))


def write_super_snps_true(snps):
    for snp in snps:
        snp_out = snp
        snp_out.append(str(True))
        print('\t'.join(snp_out))


def are_equal(snp1_chrom, snp1_pos, snp1_ref, snp1_alt, snp2_chrom, snp2_pos, snp2_ref, snp2_alt):
    if [snp1_chrom, snp1_pos, snp1_ref, snp1_alt] == [snp2_chrom, snp2_pos, snp2_ref, snp2_alt]:
        return True
    else:
        return False



def snp1_less_than_snp2(snp1_chrom, snp1_pos, snp2_chrom, snp2_pos):
    if chrom1_less_than_chrom2(snp1_chrom, snp2_chrom):
        return True
    elif snp1_pos < snp2_pos:
        return True


def chrom1_less_than_chrom2(chrom1, chrom2):
    chrom_order = ['chrM', 'chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11',
                   'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19', 'chr20', 'chr21', 'chr22',
                   'chrX',  'chrY']

    if chrom_order.index(chrom1) < chrom_order.index(chrom2):
        return True
    else:
        return False


def get_superset_reader(superset_path, header=True):
    with open(superset_path) as infile:
        if header:
            yield infile.readline().strip().split('\t')

        line = infile.readline().strip().split('\t')
        outchrom, outpos, outref, outalt, outsnps = line[0], int(line[1]), line[2], line[3], [line]
        for line in infile:
            line = line.strip().split('\t')
            chrom, pos, ref, alt = line[0], int(line[1]), line[2], line[3]

            if [chrom, pos, ref, alt] == [outchrom, outpos, outref, outalt]:
                outsnps.append(line)
            else:
                yield outchrom, outpos, outref, outalt, outsnps
                outchrom, outpos, outref, outalt, outsnps = chrom, pos, ref, alt, [line]

        yield outchrom, outpos, outref, outalt, outsnps



def get_subset_reader(vcf_reader):
    for snp in vcf_reader:
        chrom, pos, ref, alt = snp.CHROM, snp.POS, snp.REF, snp.ALT[0]
        yield chrom, pos, ref, alt, snp


if __name__ == '__main__':
    super_set_path = sys.argv[1]
    subset_vcf_path = sys.argv[2]
    column_name = sys.argv[3]

    merge_info(super_set_path, subset_vcf_path, column_name)