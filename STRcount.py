#! /usr/bin/env python

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--reference', help='the reference from which the STR Graph will be generated', required=True)
parser.add_argument('--fastq', help='the baseaclled reads in fastq format', required=True)
parser.add_argument('--config', help='the config file', required=True)
parser.add_argument('--output', help='the output file', required=True)
parser.add_argument('--min-identity', type=float, default=0.50, help='only use reads with identity greater than this', required=False)
parser.add_argument('--min-aligned-fraction', type=float, default=0.8, help='require alignments cover this proportion of the query sequence', required=False)
parser.add_argument('--write-non-spanned', action='store_true', default=False, help='do not require the reads to span the prefix/suffix region', required=False)
parser.add_argument('--repeat_orientation', help='the orientation of the repeat string. + or -', required=False, default="+")
parser.add_argument('--prefix_orientation', help='the orientation of the prefix, + or -', required=False, default="+")
parser.add_argument('--suffix_orientation', help='the orientation of the suffix, + or -', required=False, default="+")
parser.add_argument('--alignment_options', help='the alignment options', required=False, default="")
parser.add_argument('--cleanup', help='do you want to clean up the temporary file?', required=False, default="yes")
parser.add_argument('--output_directory', help='the output directory for all output and temporary files', required=False, default="./")
args = parser.parse_args()

ref = args.reference
reads = args.fastq
config_file = args.config
min_id = args.min_identity
span = args.write_non_spanned
rep_orientation = args.repeat_orientation
pre_orientation = args.prefix_orientation
suf_orientation = args.suffix_orientation
opts = args.alignment_options
cleanup_flag = 0 if args.cleanup == "no" else 1
out_dir = args.output_directory
out_file = args.output

cwd = os.getcwd()

create_tmp_folder = os.system(f"mkdir {out_dir}tmp")

str_graph_generator = os.system(f"python ./scripts/genome_str_graph_generator.py --ref {ref} --config {config_file} > {out_dir}tmp/genome_str_graph.gfa")

if str_graph_generator == 0:
    print("STR Reference Graph has been generated")
else: 
    print("error::Error while Generating STR genome graph")

ga_align = os.system(f"GraphAligner -g {out_dir}tmp/genome_str_graph.gfa -f {reads} -a {out_dir}tmp/alignment.gaf -x vg {opts}")

if ga_align == 0:
    print("Reads aligned to Reference Graph")
else:
    print("error::Error in aligning the reads to the reference graph")

parse_gaf = os.system(f"python ./scripts/parse_gaf.py --input {out_dir}tmp/genome_str_graph.gfa > {out_dir}{out_file}")

if parse_gaf == 0:
    print("A read wise count has been generated")
else:
    print("error::Error in parsing the alignments")