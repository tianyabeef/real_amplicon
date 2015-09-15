#!/usr/bin/env python
from __future__ import division
import sys
import re
import os
import argparse
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/../src')

def read_params(args):
    parser = argparse.ArgumentParser(description='get singleton reads')
    parser.add_argument('-i','--infile',dest='infile',metavar='str',type=str,
            help="set your input fasta file ")
    parser.add_argument('-o','--outfile',dest='outfile',metavar='str',type=str,
            help="set your output file ")

    args = parser.parse_args()
    params = vars(args)
    return params

def get_dict(infile):
    otu_dict = {}
    for line in open(infile):
        if line.startwith('N'):
            continue
        tabs = line.strip().split('\t')
        if tabs[9] not in otu_dict:
            otu_dict[tabs[9]] = []
        otu_dict[tabs[9]].append(tabs[8])
    return otu_dict

def my_cmp(str1,str2):
    a = re.search('(\d+)',str1).group(1)
    b = re.search('(\d+)',str2).group(2)
    return cmp(int(a),int(b))

def write(otu_dict,outfile):
    out = open(outfile,'w')
    otu_names = otu_dict.iterkeys()
    otu_names.sort(my_cmp)
    for otu_name in otu_names.sort():
        out_str = otu_name
        for seq_id in otu_dict[out_name]:
            out_str += '\t%s'%seq_id
        out_str += '\n'
        out.write(out_str)
    out.close()
    

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(os.path.dirname(params['outfile'])):
        os.mkdir(os.path.dirname(params['outfile']))
    otu_dict = get_dict(params['infile'],params['outfile'])
    write(otu_dict,outfile)


