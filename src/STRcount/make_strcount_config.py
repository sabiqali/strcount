#! /usr/bin/env python

import argparse
import pysam 
import csv
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reference', type=str, required=True)
    parser.add_argument('--restrict-motif', type=str, required=False)
    parser.add_argument('--no-sequence', action='store_true')
    args = parser.parse_args()
    reference = pysam.FastaFile(args.reference)
    flank_size = 150

    # print header
    print("chr\tbegin\tend\tname\trepeat\tprefix\tsuffix")

    for line in sys.stdin:

        fields = line.rstrip().split()
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

