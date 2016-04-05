# convert aligned sequences back to a fastq file so we can realign
java -jar ~/cgs/software/picard-tools-1.93/SamToFastq.jar I=OC57_index2_S2_L002_R1_001.strip.ribosmall.1mill.sam F=OC57_index2_S2_L002_R1_001.strip.ribosmall.1mill.fastq
ln -s OC57_index2_S2_L002_R1_001.strip.ribosmall.1mill.fastq query.fq

# align the reads to a unified reference sequence
~/cgs/software/bwa-git/bwa index ref.fa
~/cgs/software/bwa-git/bwa bwasw -t 8 -z 10 -T 10 -N 2 -b 1 ref.fa query.fq > realigned.sam
~/cgs/software/samtools-git/samtools calmd realigned.sam ref.fa > tmp.sam
mv tmp.sam realigned.sam

# align simple test sequences
# ~/cgs/software/bwa-git/bwa bwasw -t 8 -z 10 -T 10 -N 2 -b 1 ref.fa test.fa > test.sam
# ~/cgs/software/samtools-git/samtools calmd test.sam ref.fa > test_with_md.sam
# samtools view -XS test_with_md.sam

python sam_to_binary_counts.py realigned.sam > realigned_bitvectors.txt

python sam_to_allele_labels.py OC57_index2_S2_L002_R1_001.strip.ribosmall.1mill.sam > OC57_index2_S2_L002_R1_001.strip.ribosmall.1mill.assigned.txt
