import sys
import pysam

sam = pysam.AlignmentFile(sys.argv[1], "r")

target = "ATCTCTTTTCTTCTCTGTGCGAGGATTTGGACTGGCAGTG"
key_pos = 16 # index of the "key" SNP

for read in sam:
    if read.is_unmapped: continue

    pos = read.reference_start
    cigar = read.cigarstring
    md = read.get_tag("MD")
    # print pos, cigar, md, read.cigartuples

    if "^" in md or "D" in cigar or "I" in cigar:
        # Indels confuse me, so let's skip them altogether
        print >>sys.stderr, "skipping", read.query_name, cigar, md
        continue

    output = ["?"] * len(target)
    muts = 0
    key_base = "?"

    for read_pos, targ_pos, base in read.get_aligned_pairs(with_seq=True, matches_only=True):
        if targ_pos == key_pos:
            key_base = read.query_sequence[read_pos]
        if base != target[targ_pos]: # per pysam, "substitutions are lower case", which is why this works
            assert(read.query_sequence[read_pos] != target[targ_pos])
            output[targ_pos] = "1"
            muts += 1
        else:
            output[targ_pos] = "0"

    print read.query_name, "".join(output), muts, key_base
