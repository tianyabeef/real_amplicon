#!/usr/bin/env python
from __future__ import division
import sys
import re
import os
import argparse
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/../src')
from Bio import SeqIO

def read_params(args):
    parser = argparse.ArgumentParser(description='get singleton reads')
    parser.add_argument('-i','--infile',dest='infile',metavar='str',type=str,
            help="set your input fasta file ")
    parser.add_argument('-o','--outfile',dest='outfile',metavar='str',type=str,
            help="set your output file ")
    parser.add_argument('--with_size',dest='if_with_size',metavar='bool',type=bool,default=False
            help="if you set this True, a size will be added to the seq id")
    parser.add_argument('--prefix',dest='prefix',metavar='str',type=str,default='denovo'
            help="set the prefix of the id , default is [denovo]")

    args = parser.parse_args()
    params = vars(args)
    return params

def work(infile,outfile,prefix,if_with_size):
    otu_num = 0
    out = open(outfile,'w')
    for record in SeqIO.parse(open(infile),'fasta'):
        otu_num += 1
        id = '%s%s'%(prefix,otu_num)
        if if_with_size:
            try:
                size = re.search(';size=(\d+)').group(1)
                id = '%s;size=%s'%(id,size) 
            except:
                pass
        record.id = id
        record.description = ''
        out.write(record.format('fasta'))
    out.close()

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(os.path.dirname(params['outfile'])):
        os.mkdir(os.path.dirname(params['outfile']))
    work(params['infile'],params['outfile'],params['prefix'],params['if_with_size']) 
