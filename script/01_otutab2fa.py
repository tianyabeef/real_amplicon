#!/usr/bin/env python
from __future__ import division
import sys
import os
import argparse
from Bio import SeqIO

def read_params(args):
    parser = argparse.ArgumentParser(description='pick seqs in fasta_in with otutab | v1.0 at 2015/09/16 by liangzb')
    parser.add_argument('-i','--infile',dest='infile',metavar='FILE',type=str,required=True,
            help="set your input fasta file ")
    parser.add_argument('-t','--table',dest='table',metavar='FILE',type=str,required=True,
            help="set your otutab file")
    parser.add_argument('-o','--outfile',dest='outfile',metavar='FILE',type=str,required=True,
            help="set your output fasta file ")

    args = parser.parse_args()
    params = vars(args)
    return params

def get_reads_set(otutab):
    reads_set = set()
    for line in open(otutab):
        tabs = line.strip().split('\t')
        tabs.pop(0)
        for read_id in tabs:
            reads_set.add(read_id)
    return reads_set

def pickseq(infile,outfile,reads_set):
    out = open(outfile,'w')
    for record in SeqIO.parse(open(infile),'fasta'):
        if record.id not in reads_set:
            continue
        record.description = ''
        out.write(record.format('fasta'))
    out.close()

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(os.path.dirname(params['outfile'])):
        os.mkdir(os.path.dirname(params['outfile']))
    pickseq(params['infile'],params['outfile'],get_reads_set(params['table']))
