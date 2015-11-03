#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import division
import sys
import os
import re
import argparse
from util import mkdir,image_trans
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/../src')
import Parser as rp

def read_params(args):
    parser = argparse.ArgumentParser(description='tax star plot at genus level | v1.0 at 2015/10/09 by liangzb')
    parser.add_argument('-t','--tax_assignment',dest='tax_ass',metavar='FILE',type=str,required=True,
            help="set the tax assignment file")
    parser.add_argument('-i','--uniform_profile',dest='profile',metavar='FILE',type=str,required=True,
            help="set the uniform profile table")
    parser.add_argument('-o','--out_dir',dest='out_dir',metavar='DIR',type=str,required=True,
            help="set the output dir")

    args = parser.parse_args()
    params = vars(args)
    return params

def get_file_for_star_plot(tax_ass,profile,outfile):
    tax = {}
    for line in open(tax_ass):
        tabs = line.strip().split('\t')
        taxes = tabs[1].split(';')
        for name in taxes:
            if name.startswith('g__'):
                tax[tabs[0]] = name
                break
        else:
            continue
    profile_sum = {}
    with open(profile) as f:
        head = f.next()
        head = re.sub('^(.+?)\t','genus_tax\t',head)
        for line in f:
            tabs = line.strip().split('\t')
            if tabs[0] not in tax:
                continue
            tax_name = tax[tabs[0]]
            if tax_name not in profile_sum:
                profile_sum[tax_name] = map(lambda s:float(s),tabs[1:])
            else:
                for ind,tab in enumerate(tabs[1:]):
                    profile_sum[tax_name][ind] += float(tab)
    out_fp = open(outfile,'w')
    out_fp.write(head)

    def my_cmp(a,b):
        l1 = profile_sum[a]
        l2 = profile_sum[b]
        n1 = sum(l1)
        n2 = sum(l2)
        return cmp(n2,n1)

    for tax in sorted(list(profile_sum.iterkeys()),cmp=my_cmp)[:10]:
        out_str = tax
        for profile in profile_sum[tax]:
            out_str += '\t%s'%profile
        out_fp.write(out_str.strip() + '\n')
    out_fp.close()

if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['out_dir'])
    file_for_plot = params['out_dir'] + '/for_star_plot.txt'
    get_file_for_star_plot(params['tax_ass'],params['profile'],file_for_plot)
    pdf_file = params['out_dir'] + '/tax_star.pdf'
    png_file = params['out_dir'] + '/tax_star.png'

    r_job = rp.Rparser()
    r_job.open(this_script_path + '/../src/template/02_tax_star.Rtp')
    vars = {'tax_ass_uniform':file_for_plot,
            'pdf_file':pdf_file}
    r_job.format(vars)
    r_job.write(params['out_dir'] + '/tax_star.R')
    r_job.run()
    image_trans(pdf_file,png_file)

