#! /usr/bin/env python

import argparse
import pysam 
import csv
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reference', type=str,help="The reference genome" ,required=True)
    parser.add_argument('--file', type=str,help="The regions file with the information about the STRs" ,required=True)
    parser.add_argument('--restrict-motif', type=str, help="Restrict any motifs",required=False)
    parser.add_argument('--no-sequence', action='store_true', help="No flank output", required=False)
    parser.add_argument('--flank-size', type=int, default=150, help="The flank size for each config entry", required=False)
    args = parser.parse_args()

    reference = pysam.FastaFile(args.reference)
    flank_size = args.flank_size
    str_fh = open(args.file)

    str_file_header = str_fh.readline()

    # print header
    print("chr\tbegin\tend\tname\trepeat\tprefix\tsuffix")

    for line in str_fh:
        fields = line.rstrip().split('\t')
        chrom = fields[1]
        if "bin" in fields[0] or "alt" in chrom or "random" in chrom or "chrUn" in chrom:
            continue

        start = int(fields[2])
        end = int(fields[3])
        (count, motif) = fields[4].split('x')
        if args.restrict_motif is not None and args.restrict_motif != motif:
            continue

        if not args.no_sequence:
            prefix = reference.fetch(chrom, start - flank_size, start)
            suffix = reference.fetch(chrom, end, end + flank_size)
        else:
            prefix = "n/a"
            suffix = "n/a"
        name = fields[4]

        print(f"{chrom}\t{start}\t{end}\t{name}\t{motif}\t{prefix}\t{suffix}")
           
if __name__ == "__main__":
    main()

