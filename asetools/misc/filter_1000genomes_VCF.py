import vcf, sys
from glob import glob


def process_vcf(input_vcf, genomes_1000_path, out_path):
    genomes_1000_paths = glob(genomes_1000_path + '/*chr*.vcf.gz')

    genomes_reader = get_genomes_reader(genomes_1000_paths)
    #print(genomes_reader.keys())

    snp_reader = vcf.Reader(filename=input_vcf)

    outfile = open(out_path, 'w')

    outfile.write('\t'.join('CHROM POS REF ALT SAMPLE IN_1000GENOMES ID AF GQ DP REF_DP ALT_DP HOM_REF_PHRED HET_PHRED '
                    'HOM_ALT_PHRED'.split())+'\n')

    query_snp = get_first_valid_query_snp(snp_reader, genomes_reader, outfile)
    comp_snp_batch = fetch_snp_chunk(genomes_reader, query_snp)
    comp_snp, comp_snp_batch, query_snp = get_next_comp_snp(comp_snp_batch, genomes_reader, query_snp, snp_reader, outfile)

    while True:
        try:
            #print(query_snp, comp_snp)
            if snp1_less_than_snp2(query_snp.CHROM, query_snp.POS, comp_snp.CHROM, comp_snp.POS):
                write_1000G_false(query_snp, outfile)
                query_snp = next(snp_reader)

            elif chrom1_less_than_chrom2(comp_snp.CHROM, query_snp.CHROM):
                comp_snp, comp_snp_batch, query_snp = get_next_comp_snp(comp_snp_batch, genomes_reader, query_snp, snp_reader, outfile)

            elif snp1_less_than_snp2(comp_snp.CHROM, comp_snp.POS, query_snp.CHROM, query_snp.POS):
                comp_snp, comp_snp_batch, query_snp = get_next_comp_snp(comp_snp_batch, genomes_reader, query_snp,
                                                                        snp_reader, outfile, next_query_snp=True)

            elif are_equal(query_snp.CHROM, query_snp.POS, query_snp.REF, query_snp.ALT,
                           comp_snp.CHROM, comp_snp.POS, comp_snp.REF, comp_snp.ALT):
                write_1000G_true(query_snp, comp_snp, outfile)

                query_snp = next(snp_reader)
                comp_snp, comp_snp_batch, query_snp = get_next_comp_snp(comp_snp_batch, genomes_reader, query_snp, snp_reader, outfile)


            elif different_alleles(query_snp.CHROM, query_snp.POS, query_snp.REF, query_snp.ALT,
                                   comp_snp.CHROM, comp_snp.POS, comp_snp.REF, comp_snp.ALT):
                comp_snp, comp_snp_batch, query_snp = get_next_comp_snp(comp_snp_batch, genomes_reader, query_snp,
                                                                        snp_reader, outfile, next_query_snp=True)


            else:
                print(query_snp, comp_snp)
                print("ERROR")
                sys.exit()
        except StopIteration:
            break


    outfile.close()


def write_1000G_false(snp, outfile):
    for samp in snp.samples:
        name, GT, GQ, DP, REF_DP, ALT_DP, HOM_REF_PHRED, HET_PHRED, HOM_ALT_PHRED = get_sample_fields(samp)
        out = '\t'.join(map(str, [snp.CHROM, snp.POS, snp.REF, snp.ALT[0], name, False, 'NA', 'NA', GT, GQ, DP, REF_DP,
                                  ALT_DP, HOM_REF_PHRED, HET_PHRED, HOM_ALT_PHRED]))
        #print(out)
        outfile.write(out + '\n')


def write_1000G_true(query_snp, comp_snp, outfile):
    for samp in query_snp.samples:
        name, GT, GQ, DP, REF_DP, ALT_DP, HOM_REF_PHRED, HET_PHRED, HOM_ALT_PHRED = get_sample_fields(samp)
        ID, AF = get_thousands_genomes_fields(comp_snp, query_snp)
        out = '\t'.join(map(str, [query_snp.CHROM, query_snp.POS, query_snp.REF, query_snp.ALT[0], name,
                                  True, ID, AF, GT, GQ, DP, REF_DP, ALT_DP, HOM_REF_PHRED, HET_PHRED,
                                  HOM_ALT_PHRED]))
        #print(out)
        outfile.write(out + '\n')


def are_equal(snp1_chrom, snp1_pos, snp1_ref, snp1_alt, snp2_chrom, snp2_pos, snp2_ref, snp2_alt):
    snp1_chrom, snp2_chrom = [format_chrom(snp1_chrom), format_chrom(snp2_chrom)]

    if [snp1_chrom, snp1_pos, snp1_ref] == [snp2_chrom, snp2_pos, snp2_ref] and equal_alts(snp1_alt, snp2_alt):
        return True
    else:
        return False

def equal_alts(snp_alt1, snp_alt2):
    for alt1 in snp_alt1:
        for alt2 in snp_alt2:
            if alt1 == alt2:
                return True
    else:
        return False


def different_alleles(snp1_chrom, snp1_pos, snp1_ref, snp1_alt, snp2_chrom, snp2_pos, snp2_ref, snp2_alt):
    snp1_chrom, snp2_chrom = [format_chrom(snp1_chrom), format_chrom(snp2_chrom)]
    if [snp1_chrom, snp1_pos] == [snp2_chrom, snp2_pos] and [snp1_ref, snp1_alt] != [snp2_ref, snp2_alt]:
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
    chrom1, chrom2 = [format_chrom(chrom1), format_chrom(chrom2)]
    if chrom_order.index(chrom1) < chrom_order.index(chrom2):
        return True
    else:
        return False

def format_chrom(chrom):
    if not chrom.startswith('chr'):
        return 'chr'+chrom
    else:
        return chrom

def get_thousands_genomes_fields(snp_comp, snp_query):
    index = get_alt_overlap_index(snp_comp.ALT, snp_query.ALT)
    return snp_comp.ID, snp_comp.INFO['AF'][index]

def get_alt_overlap_index(snp_alt1, snp_alt2):

    for alt1 in range(len(snp_alt1)):
        for alt2 in range(len(snp_alt2)):
            if snp_alt1[alt1] == snp_alt2[alt2]:
                return alt1
    else:
        return 0

def get_sample_fields(samp_call):
    keys = samp_call.data._asdict().keys()

    name = samp_call.sample

    if 'GT' in keys:
        GT = samp_call['GT']
        if GT == '0/0':
            GT = "HOM_REF"
        elif GT == '0/1':
            GT = "HET"
        elif GT == '1/1':
            GT = "HOM_ALT"
        elif GT == './.':
            GT = "MISSING"
        elif GT == '.':
            GT = "MISSING"
        else:
            print("ERROR")
            print(GT)
            sys.exit()
    else:
        GT = 'NA'

    if 'GQ' in keys:
        GQ = samp_call['GQ']
        if not GQ:
            GQ = 'NA'
    else:
        GQ = 'NA'

    if 'DP' in keys:
        DP = samp_call['DP']
        if not DP:
            DP = 'NA'
    else:
        DP = 'NA'

    if 'AD' in keys:
        try:
            REF_DP, ALT_DP = samp_call['AD']
        except:
            REF_DP, ALT_DP = ['NA', 'NA']
    else:
        REF_DP, ALT_DP = ['NA', 'NA']

    if 'PL' in keys:
        try:
            HOM_ALT_PHRED, HET_PHRED, HOM_REF_PHRED = samp_call['PL']
        except:
            HOM_ALT_PHRED, HET_PHRED, HOM_REF_PHRED = ['NA', 'NA', 'NA']
    else:
        HOM_ALT_PHRED, HET_PHRED, HOM_REF_PHRED = ['NA', 'NA', 'NA']

    return name, GT, GQ, DP, REF_DP, ALT_DP, HOM_REF_PHRED, HET_PHRED, HOM_ALT_PHRED


def same_snp(query, comp):
    if [query.CHROM, query.POS, query.REF, query.ALT] == ['chr' + comp.CHROM, comp.POS, comp.REF, comp.ALT]:
        return True

    elif [query.CHROM, query.POS, query.REF, query.ALT] == [comp.CHROM, comp.POS, comp.REF, comp.ALT]:
        return True

    else:
        return False

def get_genomes_reader(genome_vcf_paths):
    #print('\n'.join(genome_vcf_paths))
    genomes_reader = {}
    for path in genome_vcf_paths:
        chrom = path.split('chr')[1].split('.')[0]
        chrom = 'chr' + chrom
        genomes_reader[chrom] = vcf.Reader(filename=path)

    return genomes_reader


def get_first_valid_query_snp(snp_reader, genomes_reader, outfile):
    query_snp = next(snp_reader)
    while query_snp.CHROM not in genomes_reader:
        write_1000G_false(query_snp, outfile)
        query_snp = next(snp_reader)

    return query_snp


def get_next_comp_snp(comp_snp_batch, genomes_reader, query_snp, query_snp_reader, outfile, next_query_snp=False):
    try:
        comp_snp = next(comp_snp_batch)

    except StopIteration:
        while True:
            try:
                if next_query_snp:
                    write_1000G_false(query_snp, outfile)
                    query_snp = next(query_snp_reader)

                comp_snp_batch = fetch_snp_chunk(genomes_reader, query_snp)
                comp_snp = next(comp_snp_batch)
            except StopIteration:
                write_1000G_false(query_snp, outfile)
                query_snp = next(query_snp_reader)
                continue
            break

    return comp_snp, comp_snp_batch, query_snp


def fetch_snp_chunk(genomes_reader, query_snp, batch_size=10):

    for snp in genomes_reader[query_snp.CHROM].fetch(query_snp.CHROM.strip('chr'), int(query_snp.POS) - 1,
                                                         int(query_snp.POS)+batch_size):
        yield snp


if __name__ == "__main__":
    input_vcf = sys.argv[1]
    genomes_1000_path = sys.argv[2]
    out_path = sys.argv[3]

    process_vcf(input_vcf, genomes_1000_path, out_path)