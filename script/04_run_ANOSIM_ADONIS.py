#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import division
import sys
import argparse
import os
from util import mkdir

this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')


def read_params(args):
    parser = argparse.ArgumentParser(description='''a wrapper for compare_categories | v1.0 at 2015/11/2 by liangzb ''')
    parser.add_argument('--compare_categories', dest='compare_categories', metavar='SOFT', type=str,
                        default='compare_categories.py',
                        help="set the compare_categories.py, default find in env")
    parser.add_argument('-d', '--beta_div_dir', dest='beta_dir', metavar='DIR', type=str, required=True,
                        help="set the beta div dir, produced by beta_diversity.py")
    parser.add_argument('-m', '--mapfile', dest='mapfile', metavar='FILE', type=str, required=True,
                        help="set the mapfile produced by 04_make_mapfile.py")
    parser.add_argument('-o', '--out_dir', dest='out_dir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    args = parser.parse_args()
    params = vars(args)
    return params


def work(params, name):
    commands = []
    file = os.popen('ls %s/%s*.txt' % (params['beta_dir'], name)).read().strip()
    with open(params['mapfile']) as fp:
        head = fp.next().strip()
        group_names = head.split('\t')[1:]
    for method in ['anosim', 'adonis']:
        for group_name in group_names:
            outdir = '%s/%s_%s_%s_out' % (params['out_dir'], name, group_name, method)
            mkdir(outdir)
            commands.append('%s --method %s -i %s -m %s -o %s -c %s' % (params['compare_categories'],
                                                                        method,
                                                                        file,
                                                                        params['mapfile'],
                                                                        outdir,
                                                                        group_name))
    return commands


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['out_dir'])
    commands = []
    for name in ['weighted_unifrac', 'unweighted_unifrac']:
        commands += work(params, name)
    with open('%s/commands.sh' % params['out_dir'], 'w') as out:
        out.write('\n'.join(commands))
    for command in commands:
        os.system(command)
