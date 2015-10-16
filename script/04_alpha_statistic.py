#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import division
import sys
import argparse
import os

def read_params(args):
    parser = argparse.ArgumentParser(description='''alpha statistic | v1.0 at 2015/10/16 by liangzb ''')
    parser.add_argument('-a','--alpha_collate_dir',dest='alpha_dir',metavar='DIR', type=str, required=True,
                        help="set the alpha_collate_dir")
    parser.add_argument('-m','--alpha_metrics',dest='alpha_metrics',metavar='STR',type=str,
                        default="chao1,observed_species,PD_whole_tree,shannon,simpson,goods_coverage",
                        help="set the alpha_metrics split by ',',\
                              [default is chao1,observed_species,PD_whole_tree,shannon,simpson,goods_coverage] ")
    parser.add_argument('-o','--out_tsv',dest='out_tsv',metavar='FILE',type=str,required=True,
                        help="set the output tsv file")
    args = parser.parse_args()
    params = vars(args)
    return params

def work_single(file):
    alphas = {}
    with open(file) as fp:
        samples = fp.next().strip().split('\t')[3:]
        for tail in fp:
            pass
        tail = tail.strip().split()[3:]
    for ind,sample in enumerate(samples):
        alphas[sample] = tail[ind]
    return alphas

def work_all(params):
    table = {}
    out_str = 'alpha_name'
    for alpha_name in params['alpha_metrics'].split(','):
        out_str += '\t%s'%alpha_name
        file = '%s/%s.txt'%(params['alpha_dir'],alpha_name)
        alphas = work_single(file)
        table[alpha_name] = alphas
    with open(params['out_tsv'],'w') as fp:
        fp.write(out_str.strip() + '\n')
        for sample_name in alphas.iterkeys():
            out_str = sample_name
            for alpha_name in params['alpha_metrics'].split(','):
                value = table[alpha_name][sample_name]
                out_str += '\t%s'%value
            fp.write(out_str.strip() + '\n')

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(os.path.dirname(params['out_tsv'])):
        os.mkdir(os.path.dirname(params['out_tsv']))

    work_all(params)
