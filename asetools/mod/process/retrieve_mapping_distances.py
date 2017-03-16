import sys
import pysam

def calc_mapping_distance(read1, read2):

    if read1.is_unmapped or read2.is_unmapped:
        return None
    else:
        reference_positions = [read1.reference_start, read1.reference_end-1,
                               read2.reference_start, read2.reference_end-1]
        distance = max(reference_positions) - min(reference_positions)
        return distance

def retrieve_mapping_distances(chrom, position, ref, alt, bamfile):

    ref_read_distances = []
    alt_read_distances = []

    for pileupcolumn in samfile.pileup(chrom, position, position+1, truncate=True):

        for pileupread in pileupcolumn.pileups:
            if not pileupread.is_del and not pileupread.is_refskip:
                read1 = pileupread.alignment
                allele = read1.query_sequence[pileupread.query_position]
                try:
                    read2 = samfile.mate(read1)
                except ValueError:
                    continue

                distance = calc_mapping_distance(read1, read2)

                if distance:
                    if allele == ref:
                        ref_read_distances.append(distance)
                    elif allele == alt:
                        alt_read_distances.append(distance)



    return sorted(ref_read_distances), sorted(alt_read_distances)



def complementary_base(base):
    if base == 'A':
        return 'T'
    elif base == 'T':
        return 'A'
    elif base == 'G':
        return 'C'
    elif base == 'C':
        return 'G'
    else:
        return base


if __name__ == '__main__':
    # USAGE:

    bamfile_in = sys.argv[1]
    chrom = sys.argv[2]
    pos = int(sys.argv[3])-1
    ref = sys.argv[4]
    alt = sys.argv[5]

    samfile = pysam.AlignmentFile(bamfile_in, "rb")

    ref_read_distances, alt_read_distances = retrieve_mapping_distances(chrom, pos, ref, alt, samfile)
    print("REF: "+' '.join([str(i) for i in ref_read_distances]))
    print("ALT: " + ' '.join([str(i) for i in alt_read_distances]))