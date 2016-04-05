import sys
import pysam

sam = pysam.AlignmentFile(sys.argv[1], "r")

for read in sam:
    if read.is_unmapped: continue

    ref = read.reference_name

    as_tag = read.get_tag("AS")
    xs_tag = read.get_tag("XS") if read.has_tag("XS") else None

    if as_tag == xs_tag:
        ref = "?"

    print read.query_name, ref
