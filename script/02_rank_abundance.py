#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import division
import sys
import os
import argparse
from util import mkdir, image_trans


def read_params(args):
    parser = argparse.ArgumentParser(description='a wrapper for rank_abundance | v1.0 at 2015/10/09 by liangzb')
    parser.add_argument('-s', '--rank_abundance', dest='rank_abundance', metavar='STR', type=str,
                        default='plot_rank_abundance_graph.py',
                        help="set the plot_rank_abundance_graph.py with absolute path, default find in env")
    parser.add_argument('-i', '--biom_file', dest='biomfile', metavar='FILE', type=str, required=True,
                        help="set the input biom file")
    parser.add_argument('-o', '--out_dir', dest='out_dir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    parser.add_argument('--legend', dest='legend', action='store_true',
                        help="plot with legend")
    parser.add_argument('--no_legend', dest='legend', action='store_false',
                        help="plot without legend")
    parser.set_defaults(legend=False)
    parser.add_argument('--log', dest='draw_log', action='store_true',
                        help='draw axis in log scale, [default]')
    parser.add_argument('--linear', dest='draw_log', action='store_false',
                        help='draw axis in linear scale')
    parser.set_defaults(draw_log=True)
    parser.add_argument('--absolute', dest='absolute', action='store_true',
                        help='plot absolute abundance')
    parser.add_argument('--relative', dest='absolute', action='store_false',
                        help='plot ralative abundance, [default]')
    parser.set_defaults(absolute=False)

    args = parser.parse_args()
    params = vars(args)
    return params


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['out_dir'])
    pdf_file = '%s/rank_abundance.pdf' % params['out_dir']
    png_file = '%s/rank_abundance.png' % params['out_dir']
    if params['legend']:
        command = "%s -i %s -s '*' -o %s" % (params['rank_abundance'],
                                             params['biomfile'],
                                             pdf_file)
    else:
        command = "%s -i %s -s '*' -o %s --no_legend" % (params['rank_abundance'],
                                                         params['biomfile'],
                                                         pdf_file)
    if not params['draw_log']:
        command += ' --x_linear_scale --y_linear_scale'
    if params['absolute']:
        command += ' --absolute_counts'
    os.system(command)
    image_trans(pdf_file, png_file)
