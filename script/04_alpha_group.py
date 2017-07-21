#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import division
import sys
import argparse
import os
from util import mkdir
import pandas as pd
this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
from Parser import parse_group_file


def read_params(args):
    parser = argparse.ArgumentParser(description='''alpha grouped | v1.0 at 2015/10/15 by liangzb ''')
    parser.add_argument('-a', '--alpha_collate_dir', dest='alpha_dir', metavar='DIR', type=str, required=True,
                        help="set the alpha_collate_dir")
    parser.add_argument('-g', '--group', dest='group', metavar='FILE', type=str, required=True,
                        help="set the group file")
    parser.add_argument('-m', '--alpha_metrics', dest='alpha_metrics', metavar='STR', type=str,
                        default="chao1,observed_species,PD_whole_tree,shannon,simpson,goods_coverage",
                        help="set the alpha_metrics split by ',',\
                              [default is chao1,observed_species,PD_whole_tree,shannon,simpson,goods_coverage] ")
    parser.add_argument('-o', '--out_dir', dest='out_dir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    args = parser.parse_args()
    params = vars(args)
    return params


def work_single(file, group):
    alphas = {}
    with open(file) as fp:
        #samples = fp.next().rstrip().split('\t')[3:]
	samples = fp.next().rstrip().split('\t')[1:]
        for tail in fp:
            pass
        #tail = tail.rstrip().split()[3:]
	tail = tail.rstrip().split()[1:]	
    for ind, sample in enumerate(samples):
        group_name = group[sample]
        if group_name not in alphas:
            alphas[group_name] = []
        if tail[ind] == "n/a":
            continue
        alphas[group_name].append(tail[ind])
    return alphas


def write(outfile, alphas, group):
    group_sort = list(group.itervalues())
    group_names = sorted(set(group_sort), key=group_sort.index)
    with open(outfile, 'w') as out:
        for group_name in group_names:
            alpha_list = alphas[group_name]
            alpha_list = '\t'.join(alpha_list)
            out.write('%s\t%s\n' % (group_name, alpha_list))


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['out_dir'])
    group = parse_group_file(params['group'])
    for alpha_name in params['alpha_metrics'].split(','):
        file = '%s/%s.txt' % (params['alpha_dir'], alpha_name)
        outfile = '%s/%s.txt' % (params['out_dir'], alpha_name)
	data = pd.DataFrame.from_csv(file,sep="\t")
        data[group.keys()].to_csv("%s_tmp"%(file),sep="\t")
	file = "%s_tmp"%(file)
        alphas = work_single(file, group)
        write(outfile, alphas, group)
