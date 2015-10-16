#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import division
import sys
import argparse
import os

def read_params(args):
    parser = argparse.ArgumentParser(description='''alpha grouped | v1.0 at 2015/10/15 by liangzb ''')
    parser.add_argument('-a','--alpha_collate_dir',dest='alpha_dir',metavar='DIR', type=str, required=True,
                        help="set the alpha_collate_dir")
    parser.add_argument('-g','--group',dest='group',metavar='FILE',type=str,required=True,
                        help="set the group file")
    parser.add_argument('-m','--alpha_metrics',dest='alpha_metrics',metavar='STR',type=str,
                        default="chao1,observed_species,PD_whole_tree,shannon,simpson,goods_coverage",
                        help="set the alpha_metrics split by ',',\
                              [default is chao1,observed_species,PD_whole_tree,shannon,simpson,goods_coverage] ")
    parser.add_argument('-o', '--out_dir', dest='out_dir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    args = parser.parse_args()
    params = vars(args)
    return params

def get_group(group_file):
    group = {}
    with open(group_file) as fp:
        for line in fp:
            tabs = line.strip().split('\t')
            group[tabs[0]] = tabs[1]
    return group

def work_single(file,group):
    alphas = {}
    with open(file) as fp:
        samples = fp.next().strip().split('\t')[3:]
        for tail in fp:
            pass
        tail = tail.strip().split()[3:]
    for ind,sample in enumerate(samples):
        group_name = group[sample]
        if group_name not in alphas:
            alphas[group_name] = []
        alphas[group_name].append(tail[ind])
    return alphas

def write(outfile,alphas):
    with open(outfile,'w') as out:
        for group,alpha_list in alphas.iteritems():
            alpha_list = '\t'.join(alpha_list)
            out.write('%s\t%s\n'%(group,alpha_list))

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(params['out_dir']):
        os.mkdir(params['out_dir'])
    group = get_group(params['group'])
    for alpha_name in params['alpha_metrics'].split(','):
        file = '%s/%s.txt'%(params['alpha_dir'],alpha_name)
        outfile = '%s/%s.txt'%(params['out_dir'],alpha_name)
        alphas = work_single(file,group)
        write(outfile,alphas)
