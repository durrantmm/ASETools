import sys
import vcf
import gzip

def convert_genotypes_to_vcf(genotypes_path, template_vcf_path):
    delim = ','

    vcf_header = get_header(template_vcf_path)
    print(vcf_header)

    with open(genotypes_path) as filein:

        header = filein.readline().strip().split(delim)


        for line in filein:
            line = line.strip().split(delim)
            snp = {header[i]:line[i] for i in range(len(line))}
            chrom, pos, ref, alt, ID = 'chr'+snp['chr_b37'], snp['pos_b37'], snp['Allele.A'], \
                                       snp['Allele.B'], snp['dbSNP.RS.ID']
            qual, filter, info = [',','.','.']
            format = 'GT'
            call = snp['simpleGenotype']
            genotype = get_genotype(ref, alt, call)

            print('\t'.join([chrom, pos, ID, ref, alt, qual, filter, info, format, genotype]))

def get_header(vcf_template):
    out_header = []
    with gzip.open(vcf_template) as filein:
        for line in filein:
            line = line.decode("utf-8").strip()
            if not line.startswith('#'):
                break
            elif line.startswith("#CHROM"):
                line = '\t'.join(line.strip().split()[:9]+['HCT116'])
                out_header.append(line)
            else:
                out_header.append(line)

    return '\n'.join(out_header)



def get_genotype(ref, alt, call):
    call = list(call)
    if call == [ref, ref]:
        return '0/0'
    elif call == [ref, alt]:
        return '0/1'
    elif call == [alt, alt]:
        return '1/1'
    else:
        return('./.')




if __name__ == '__main__':


    if True:
        # USAGE: python bak.py data/HCT-116_genotypes.csv data/ALL_HET_VARIANTS_SORTED_CHROM_ONLY.vcf.gz
        genotypes_path = sys.argv[1]
        template_vcf_path = sys.argv[2]
        convert_genotypes_to_vcf(genotypes_path, template_vcf_path)







