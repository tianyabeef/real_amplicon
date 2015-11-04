#!/usr/bin/env python
from __future__ import division
import sys
import re
import os
import argparse
from util import mkdir
from Bio import SeqIO

def read_params(args):
    parser = argparse.ArgumentParser(description='rename otu fasta with prefix | v1.0 at 2015/09/16 by liangzb')
    parser.add_argument('-i','--infile',dest='infile',metavar='FILE',type=str,required=True,
            help="set your input fasta file")
    parser.add_argument('-o','--outfile',dest='outfile',metavar='FILE',type=str,required=True,
            help="set your output file ")
    parser.add_argument('--with_size',dest='if_with_size',action='store_true',
                        help="add a size to the seq id")
    parser.add_argument('--without_size',dest='if_with_size',action='store_false',
                        help="do not add a size to the seq id")
    parser.set_defauts(if_with_size=False)
#      parser.add_argument('--with_size',dest='if_with_size',metavar='BOOL',type=bool,default=False,
#              help="if you set this True, a size will be added to the seq id, [ default is False ]")
    parser.add_argument('--prefix',dest='prefix',metavar='STR',type=str,default='denovo',
            help="set the prefix of the id , [ default is denovo ]")

    args = parser.parse_args()
    params = vars(args)
    return params

def work(infile,outfile,prefix,if_with_size):
    regex = re.compile(';size=(\d+)')
    otu_num = 0
    out = open(outfile,'w')
    for record in SeqIO.parse(open(infile),'fasta'):
        otu_num += 1
        id = '%s%s'%(prefix,otu_num)
        if if_with_size:
            size = re.search(regex,record.id).group(1)
            id = '%s;size=%s'%(id,size)
        record.id = id
        record.description = ''
        out.write(record.format('fasta'))
    out.close()

if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(os.path.dirname(params['outfile']))
    work(params['infile'],params['outfile'],params['prefix'],params['if_with_size'])
