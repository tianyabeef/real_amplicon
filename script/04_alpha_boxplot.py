#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import division
import sys
import argparse
import os
this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
import RParser as rp

def read_params(args):
    parser = argparse.ArgumentParser(description='''make tree wrapper | v1.0 at 2015/10/14 by liangzb ''')
    parser.add_argument('-a','--alpha_collate_dir',dest='alpha_dir',metavar='DIR', type=str, required=True,
                        help="set the alpha_collate_dir")
    parser.add_argument('-m','--alpha_metrics',dest='alpha_metrics',metavar='STR',type=str,
                        default="chao1,observed_species,PD_whole_tree,shannon,simpson,goods_coverage",
                        help="set the alpha_metrics split by ',',\
                              [default is chao1,observed_species,PD_whole_tree,shannon,simpson,goods_coverage] ")
    parser.add_argument('-o', '--out_dir', dest='out_dir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    args = parser.parse_args()
    params = vars(args)
    return params

def read_single(file,alpha_name,outfile):
    with open(file) as fp:
        head = fp.next().split('\t')[3:]
        head.insert(0,'alphaname')
        head = '\t'.join(head)
        for line in fp:
            pass
        tail = line.strip('\t')[3:].insert(0,alpha_name)
        tail = '\t'.join(tail)
    with open(outfile,'w') as fp:
        fp.write(head+tail)

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(params['out_dir']):
        os.mkdir(params['out_dir'])
    for alpha_name in params['alpha_metrics'].split(','):
        file = '%s/%s.txt'%(params['alpha_collate_dir'],alpha_name)
        outfile = '%s/%s.w.txt'%(params['out_dir'],alpha_name)
        pdf_file = '%s/%s.boxplot.pdf'%(params['out_dir'],alpha_name)
        png_file = '%s/%s.boxplot.png'%(params['out_dir'],alpha_name)
        read_single(file,alpha_name,outfile)
        vars = {'w_file':outfile,
                'pdf_file':pdf_file,
                'group_file':params['group']}
        r_job = rp.RParser()
        r_job.open(this_script_path + '/../src/template/04_alpha_diff_boxplot.Rtp')
        r_job.format(vars)
        r_job.write(params['out_dir'] + '/alpha_diff_boxplot.R')
        r_job.run()
        os.system('convert %s %s'%(pdf_file,png_file))
