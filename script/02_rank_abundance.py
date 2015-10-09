#!/usr/bin/env python
from __future__ import division
import sys
import os
import re
import argparse
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/../src')
import RParser as rp

def read_params(args):
    parser = argparse.ArgumentParser(description='a wrapper for rank_abundance | v1.0 at 2015/10/09 by liangzb')
    parser.add_argument('-s','--rank_abundance',dest='rank_abundance',metavar='STR',type=str,default='plot_rank_abundance_graph.py',
            help="set the plot_rank_abundance_graph.py with absolute path, default find in env")
    parser.add_argument('-i','--biom_file',dest='biomfile',metavar='FILE',type=str,required=True,
            help="set the input biom file")
    parser.add_argument('-o','--out_dir',dest='out_dir',metavar='DIR',type=str,required=True,
            help="set the output dir")

    args = parser.parse_args()
    params = vars(args)
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(params['out_dir']):
        os.mkdir(params['out_dir'])
    pdf_file = '%s/rank_abundance.pdf'%params['out_dir']
    png_file = '%s/rank_abundance.png'%params['out_dir']
    os.system("%s -i %s -s '*' -o %s --no_legend"%(params['rank_abundance'],
                                                   params['biomfile'],
                                                   pdf_file))
    os.system("convert -density '200x200^' %s %s"%(pdf_file,png_file))
