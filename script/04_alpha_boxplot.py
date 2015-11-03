#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import division
import sys
import argparse
import os
from util import mkdir,image_trans
this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
import Parser as rp

def read_params(args):
    parser = argparse.ArgumentParser(description='''alpha boxplot | v1.0 at 2015/10/14 by liangzb ''')
    parser.add_argument('-a','--alpha_grouped_dir',dest='alpha_dir',metavar='DIR', type=str, required=True,
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

if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['out_dir'])
    for alpha_name in params['alpha_metrics'].split(','):
        file = '%s/%s.txt'%(params['alpha_dir'],alpha_name)
        pdf_file = '%s/%s.boxplot.pdf'%(params['out_dir'],alpha_name)
        png_file = '%s/%s.boxplot.png'%(params['out_dir'],alpha_name)
        vars = {'grouped_file':file,
                'pdf_file':pdf_file,
                'alpha_name':alpha_name}
        r_job = rp.Rparser()
        r_job.open(this_script_path + '/../src/template/04_alpha_diff_boxplot.Rtp')
        r_job.format(vars)
        r_job.write(params['out_dir'] + '/%s_boxplot.R'%alpha_name)
        r_job.run()
        image_trans(pdf_file,png_file)
