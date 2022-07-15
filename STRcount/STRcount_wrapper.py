#! /usr/bin/env python

import argparse
import os
import logging

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
parser.add_argument('--cleanup', help='do you want to clean up the temporary file?', required=False, default="yes")
parser.add_argument('--output_directory', help='the output directory for all output and temporary files', required=False, default="./")
parser.add_argument('--multiseed-DP', help='Aligner option', required=False, default="")
parser.add_argument('--precise-clipping', help='Aligner option: use arg as the identity threshold for a valid alignment.', required=False, default="")
args = parser.parse_args()

ref = args.reference
reads = args.fastq
config_file = args.config
min_id = args.min_identity
min_align = args.min_aligned_fraction
span = args.write_non_spanned
rep_orientation = args.repeat_orientation
pre_orientation = args.prefix_orientation
suf_orientation = args.suffix_orientation
cleanup_flag = 0 if args.cleanup == "no" else 1
out_dir = args.output_directory
out_file = args.output
seed = args.multiseed_DP
id_thres = args.precise_clipping

cwd = os.getcwd()

def main():
    if min_id:
        min_id_arg = f"--min-identity {min_id}"
    else:
        min_id_arg = ""

    if span:
        span_arg = f"--write-non-spanned {span}"
    else:
        span_arg = ""

    if min_align:
        min_align_arg = f"--min-aligned-fraction {min_align}"
    else:
        min_align_arg = ""

    if rep_orientation:
        rep_orientation_arg = f"--repeat_orientation {rep_orientation}"
    else:
        rep_orientation_arg = ""

    if pre_orientation:
        pre_orientation_arg = f"--prefix_orientation {pre_orientation}"
    else:
        pre_orientation_arg = ""

    if suf_orientation:
        suf_orientation_arg = f"--suffix_orientation {suf_orientation}"
    else:
        suf_orientation_arg = ""

    if seed:
        seed_arg = f"--multiseed-DP {seed}"
    else:
        seed_arg = ""

    if id_thres:
        id_thres_arg = f"--precise-clipping {id_thres}"
    else:
        id_thres_arg = ""

    create_tmp_folder = os.system(f"mkdir {out_dir}tmp")

    str_graph_generator = os.system(f"python ./STRcount/genome_str_graph_generator.py --ref {ref} --config {config_file} {rep_orientation_arg} {pre_orientation_arg} {suf_orientation_arg} > {out_dir}tmp/genome_str_graph.gfa")

    if str_graph_generator == 0:
        logging.info("STR Reference Graph has been generated")
    else: 
        logging.error("Error while Generating STR genome graph")

    ga_align = os.system(f"GraphAligner {seed_arg} {id_thres_arg} -g {out_dir}tmp/genome_str_graph.gfa -f {reads} -a {out_dir}tmp/alignment.gaf -x vg")

    if ga_align == 0:
        logging.info("Reads aligned to Reference Graph")
    else:
        logging.error("Error in aligning the reads to the reference graph")

    parse_gaf = os.system(f"python ./STRcount/parse_gaf.py --input {out_dir}tmp/genome_str_graph.gfa {min_id_arg} {min_align_arg} {span_arg} > {out_dir}{out_file}")

    if parse_gaf == 0:
        logging.info("A read wise count has been generated")
    else:
        logging.error("Error in parsing the alignments")

if __name__ == "__main__":
    main()
