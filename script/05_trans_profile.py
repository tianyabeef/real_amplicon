#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import sys
import os
import argparse
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/../src')
from Parser import parse_group_file

def read_params(args):
    parser = argparse.ArgumentParser(description='trans_profile | v1.0 at 2015/10/19 by liangzb')
    parser.add_argument('-i','--infile',dest='infile',metavar='FILE',type=str,required=True,
                        help="set the input file")
    parser.add_argument('-o','--outfile',dest='outfile',metavar='FILE',type=str,required=True,)
    parser.add_argument('-i','--summarize_all',dest='infile',metavar='FILE',type=str,required=True,
                        help="set hte otu_table_all.txt produced by 02_summarize_trans.py")
    parser.add_argument('-l','--LEfSe_path',dest='LEfSe_path', metavar='DIR',type=str,default=None,
                        help="set the LEfSe path, default find in env")
    parser.add_argument('-g','--group_file', dest='group', metavar='FILE',type=str,required=True,
                        help="set the group file")
    parser.add_argument('-o','--out_dir', dest='out_dir', metavar='DIR',type=str,required=True,
                        help="set the output dir")
    args = parser.parse_args()
    params = vars(args)
    if params['LEfSe_path'] is None:
        params['LEfSe_path'] = ''
    else:
        params['LEfSe_path'] += '/'
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(params['out_dir']):
        os.mkdir(params['out_dir'])
    group = parse_group_file(params['group'])
    for_analysis = '%s/otu_table_for_lefse.txt'%params['out_dir']

