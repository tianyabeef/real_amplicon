#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import division
import sys
import argparse
import os
from util import mkdir,image_trans
this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
from Parser import parse_stat_file

def read_params(args):
    parser = argparse.ArgumentParser(description='''beta cluster wrapper | v1.0 at 2015/10/16 by liangzb ''')
    parser.add_argument('--jackknifed_beta_diversity',dest='jack_soft',metavar='STR',type=str,default="jackknifed_beta_diversity.py",
                        help="set the jackknifed_beta_diversity.py, default find in env")
    parser.add_argument('--make_bootstrapped_tree',dest='bootstrap_soft',metavar='STR',type=str,default="make_bootstrapped_tree.py",
                        help="set the make_bootstrapped_tree.py, default find in env")
    parser.add_argument('-i','--otu_biom',dest='otu_biom',metavar='FILE',type=str,required=True,
                        help="set the otu biom file")
    parser.add_argument('-t','--tree_file',dest='tree_file',metavar='FILE',type=str,required=True,
                        help="set the tree file")
    parser.add_argument('-g','--group_file',dest='group_file',metavar='FILE',type=str,default=None,
                        help="set the group file")
    parser.add_argument('-s','--seqs_per_sample',dest='seqs',metavar="INT",type=int,default=None,
                        help="set the seqs_per_sample, can be overrited if set stat_file")
    parser.add_argument('--stat_file',dest='stat_file',metavar='FILE',type=str,default=None,
                        help="set the stat file produced by 01_stat.py")
    parser.add_argument('-o', '--out_dir', dest='out_dir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    args = parser.parse_args()
    params = vars(args)
    if params['stat_file'] is not None:
        maximum,minimum = parse_stat_file(params['stat_file'],group_file=params['group_file'])
        params['seqs'] = minimum
    if params['seqs'] is None and params['stat_file'] is None:
        parser.print_help()
        sys.exit()
    return params

def convert_mapfile(group_file,mapfile):
    with open(group_file) as in_fp,open(mapfile,'w') as out_fp:
        out_fp.write('#SampleID\tDescription\n')
        out_fp.write('#Example mapping file for the QIIME analysis package.\n')
        out_fp.write(in_fp.read())

def work(name,params):
    cmp_dir = '%s/%s/upgma_cmp'%(params['out_dir'],name)
    tree = '%s/master_tree.tre'%cmp_dir
    support = '%s/jackknife_support.txt'%cmp_dir
    pdf = '%s/%s_cluster.pdf'%(params['out_dir'],name)
    png = '%s/%s_cluster.png'%(params['out_dir'],name)
    command = '%s -m %s -s %s -o %s'%(params['bootstrap_soft'],
                                      tree,
                                      support,
                                      pdf)
    os.system(command)
    image_trans(pdf,png)
    return command

if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['out_dir'])

    commands = []
    mapfile =  '%s/mapfile.txt'%params['out_dir']
    convert_mapfile(params['group_file'],mapfile)
    command = '%s -i %s -e %s -t %s -m %s -o %s -f'%(params['jack_soft'],
                                                     params['otu_biom'],
                                                     params['seqs'],
                                                     params['tree_file'],
                                                     mapfile,
                                                     params['out_dir'])
    commands.append(command)
    os.system(command)
    for name in ['weighted_unifrac','unweighted_unifrac']:
        command = work(name,params)
        commands.append(command)
    with open(params['out_dir'] + '/commands.sh','w') as out:
        out.write('\n'.join(commands))
