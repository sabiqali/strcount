#! /usr/bin/env python
import sys
import pysam
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--ref', help='the ref file', required=True)
parser.add_argument('--config', help='the config file', required=True)
parser.add_argument('--repeat_orientation', help='the orientation of the repeat string. + or -', required=False, default="+")
parser.add_argument('--prefix_orientation', help='the orientation of the prefix, + or -', required=False, default="+")
parser.add_argument('--suffix_orientation', help='the orientation of the suffix, + or -', required=False, default="+")

args = parser.parse_args()

reference_file = args.ref
config = args.config
repeat_orientation = args.repeat_orientation
prefix_orientation = args.prefix_orientation
suffix_orientation = args.suffix_orientation

# read in the configs and store them in the respective variables
configs = list()
config_fh = open(config)
header = config_fh.readline()

for line in config_fh:
    configs.append(line.rstrip().split()[0:7])

configs_dict = dict()

#In this case I am extracting only 1 config but in case we have more than 1, we can have a loop here to extract the other configs
for chromosome,begin,end,name,repeat,prefix,suffix in configs:
    configs_dict[name] = [chromosome,begin,end,name,repeat,prefix,suffix]

print("H\tVN:Z:a.0")

#appraoch it chromosome wise and then have a variable for sides and one for links for the chromosome and then in the end iterate over all and print. 

sides = dict()
links = dict()

counter1 = 0

for chr in pysam.FastxFile(reference_file):
    counter2 = 0
    key_list = []
    for keys in configs_dict:
        if(chr.name == configs_dict[keys][0]):
            counter2 += 1
            key_list.append(keys)

    if counter2 == 1:
        counter1 += 1
        sides[chr.name] = "\t".join(["S", chr.name + "_before_prefix", chr.sequence[: int(configs_dict[key_list[0]][1])-(len(configs_dict[key_list[0]][5])+1) ]]) + "\n" + "\t".join(["S", chr.name + "_prefix", chr.sequence[int(configs_dict[key_list[0]][1])-(len(configs_dict[key_list[0]][5])+1) : int(configs_dict[key_list[0]][1])-1]]) + "\n" + "\t".join(["S", "repeat_" + configs_dict[key_list[0]][3], configs_dict[key_list[0]][4]]) + "\n" + "\t".join(["S", chr.name + "_suffix", chr.sequence[int(configs_dict[key_list[0]][2])+1 : (int(configs_dict[key_list[0]][2])+len(configs_dict[key_list[0]][6])+1)]]) + "\n" + "\t".join(["S", chr.name + "_after_suffix", chr.sequence[int(configs_dict[key_list[0]][2])+(len(configs_dict[key_list[0]][6])+1) : ]])
        links[chr.name] = "\t".join(["L", chr.name + "_before_prefix", "+", chr.name + "_prefix", prefix_orientation, "0M" ]) + "\n" + "\t".join(["L", chr.name + "_prefix", prefix_orientation , "repeat_" + configs_dict[key_list[0]][3] , repeat_orientation , "0M"]) + "\n" + "\t".join(["L", "repeat_" + configs_dict[key_list[0]][3] , repeat_orientation, "repeat_" + configs_dict[key_list[0]][3] , repeat_orientation, "0M"]) + "\n" + "\t".join(["L", "repeat_" + configs_dict[key_list[0]][3] , repeat_orientation, chr.name + "_suffix", suffix_orientation, "0M"]) + "\n" + "\t".join(["L", chr.name + "_suffix", suffix_orientation, chr.name + "_after_suffix", "+", "0M"])
    else:
        sides[chr.name] = "\t".join(["S", chr.name, chr.sequence])      

for key in sides:
    print(sides[key])

for key in links:
    print(links[key])       

if(counter1==0):
    print("Error : The chromosome of the config file was not found in the reference, please double check your inputs.")
