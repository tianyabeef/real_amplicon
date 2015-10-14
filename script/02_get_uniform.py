#!/usr/bin/env python
from __future__ import division
import sys
import os
import argparse

def read_params(args):
    parser = argparse.ArgumentParser(description='get otu profile uniform | v1.0 at 2015/09/29 by liangzb')
    parser.add_argument('-i','--infile',dest='infile',metavar='FILE',type=str,required=True,
            help="set the un-uniformed profile produced by biom convert")
    parser.add_argument('-o','--out_file',dest='outfile',metavar='FILE',type=str,required=True,
            help="set the output uniform profile")

    args = parser.parse_args()
    params = vars(args)
    return params

def get_sum(infile):
    fp = open(infile)
    sum = {}
    for line in fp:
        if line.startswith('# Constructed from'):
            continue
        if line.startswith('#'):
            heads = line.strip('#').strip().split('\t')
            continue
        tabs = line.strip().split('\t')
        for index in range(1,len(tabs)):
            if heads[index] not in sum:
                sum[heads[index]] = 0
            sum[heads[index]] += float(tabs[index])
    fp.close()
    return sum

def write(outfile,infile,sum):
    fp_in = open(infile)
    fp_out = open(outfile,'w')
    for line in fp_in:
        if line.startswith('# Constructed from'):
            continue
        if line.startswith('#'):
            fp_out.write(line.strip('#'))
            heads = line.strip('#').strip().split('\t')
            continue
        tabs = line.strip().split('\t')
        out_str = tabs[0] + '\t'
        for index in range(1,len(tabs)):
            out_str += '%s\t'%(float(tabs[index]) / sum[heads[index]])
        fp_out.write(out_str.strip() + '\n')
    fp_in.close()
    fp_out.close()

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(os.path.dirname(params['outfile'])):
        os.mkdir(os.path.dirname(params['outfile']))
    sum = get_sum(params['infile'])
    write(params['outfile'],params['infile'],sum)
