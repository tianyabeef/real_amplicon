#!/usr/bin/env python
# -*- coding: utf-8 -*- \#
"""
@author = 'liangzb'
@date = '2016-01-11'
plot tree and bar with profile
"""

import sys
import os
import argparse
from util import tax_profile_filter, mkdir, image_trans

this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
import Parser as rp


def read_params(args):
    parser = argparse.ArgumentParser(description='''tax heatmap | v1.0 at 2015/10/13 by liangzb ''')
    parser.add_argument('-i', '--otu_profile', dest='otu_table', metavar='FILE', type=str, required=None,
                        help="set the otu_table_L6.txt")
    parser.add_argument('-f', '--for_plot', dest='for_plot', metavar='FILE', type=str, default=None,
                        help="set the profile for plot, if set this param, otu_table will not work, \
                              one of otu_profile and for_plot is required")
    parser.add_argument('-g', '--group_file', dest='group', metavar='FILE', type=str, required=True,
                        help="set the group file")
    parser.add_argument('-o', '--out_dir', dest='out_dir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    parser.add_argument('-l', '--tax_level', dest='level', metavar='STR', type=str, default='genus',
                        help="set the tax level, [default is genus]")
    parser.add_argument('-t', '--top', dest='top', metavar='INT', type=str, default='20',
                        help="set the top num, [default is 20]")

    args = parser.parse_args()
    params = vars(args)
    if params['top'] != 'all':
        params['top'] = int(params['top'])
    if params['for_plot'] is None and params['otu_table'] is None:
        parser.print_help()
        sys.exit()
    return params


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['out_dir'])
    if params['for_plot'] is None:
        params['for_plot'] = params['out_dir'] + '/for_plot.txt'
        tax_profile_filter(params['otu_table'], params['for_plot'], params['level'])
    pdf_file = params['out_dir'] + '/bar_tree.pdf'
    png_file = params['out_dir'] + '/bar_tree.png'

    vars = {'profile': params['for_plot'],
            'pdf_file': pdf_file,
            'group': params['group'],
            'top': params['top'],
            }
    r_job = rp.Rparser()
    r_job.open(this_script_path + '/../src/template/03_tax_bar_tree.Rtp')
    r_job.format(vars)
    r_job.write(params['out_dir'] + '/bar_tree.R')
    r_job.run()
    image_trans(pdf_file, png_file)
