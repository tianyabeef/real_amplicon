#!/usr/bin/env python
from __future__ import division
import sys
import os
import re
import argparse
from util import mkdir

def read_params(args):
    parser = argparse.ArgumentParser(description='transform rdp out file to qiime | v1.0 at 2015/09/21 by liangzb')
    parser.add_argument('-i','--infile',dest='infile',metavar='FILE',type=str,required=True,
            help="set the input file")
    parser.add_argument('-c','--conf',dest='conf',metavar='FLOAT',type=float,default=0.8,
            help="set the confidence cutoff, [ default is 0.8 ]")
    parser.add_argument('-o','--outdir',dest='outfile',metavar='FILE',type=str,required=True,
            help="set the output file")

    args = parser.parse_args()
    params = vars(args)
    return params

class Tax(object):
    def __init__(self):
        self.tax_level = ''
        self.tax_name = ''
        self.tax_conf = 0

def my_cmp(a,b):
    n1 = re.search('(\d+)',a).group(1)
    n2 = re.search('(\d+)',b).group(1)
    return cmp(int(n1),int(n2))

short_name = {'domain':'k','phylum':'p','class':'c','order':'o','family':'f','genus':'g','species':'s'}
short_name_order = ['k','p','c','o','f','g','s']

def read_rdp(file):
    otu_tax = {}
    fp = open(file)
    for line in fp:
        tabs = line.strip().split('\t')
        otu_name = tabs[0]
        otu_tax[otu_name] = {}
        for index in range(5,len(tabs),3):
            tax = Tax()
            tax.tax_name = tabs[index].strip('"')
            tax.tax_level = tabs[index + 1]
            tax.tax_conf = float(tabs[index + 2])
            if tax.tax_level not in short_name:
                continue
            tax_short_name = short_name[tax.tax_level]
            otu_tax[otu_name][tax_short_name] = tax
    fp.close()
    return otu_tax

def write_qiime(file,otu_tax,conf):
    fp = open(file,'w')
    out_str = ''
    for otu in sorted(list(otu_tax.iterkeys()),cmp=my_cmp):
        pre_out_str = otu + '\t'
        last_conf = 0
        for short_name in short_name_order:
            if short_name not in otu_tax[otu]:
                continue
            tax = otu_tax[otu][short_name]
            if tax.tax_conf < conf:
                break
            last_conf = tax.tax_conf
            pre_out_str += '%s__%s;'%(short_name,tax.tax_name)
        if last_conf < conf:
            continue
        pre_out_str = pre_out_str.strip(';')
        pre_out_str += '\t%s\n'%last_conf
        out_str += pre_out_str
    fp.write(out_str)
    fp.close()

if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(os.path.dirname(params['outfile']))
    otu_tax = read_rdp(params['infile'])
    write_qiime(params['outfile'],otu_tax,params['conf'])

