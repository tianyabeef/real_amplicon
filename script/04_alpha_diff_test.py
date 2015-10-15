#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import division
import sys
import argparse
import os
this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
import RParser as rp

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

class Group(object):
    def __init__(self,group_name):
        self.name = group_name
        self.alpha_mean = {}

def write(marker_files,total_marker):
    groups = {}
    p_values = []
    alpha_names = []
    for marker_file in marker_files:
        with open(marker_files) as mf:
            group_names = mf.next().strip().split('\t')[1:-1]
            for group_name in group_names:
                if group_name not in groups:
                    groups[group_name] = Group(group_name)
            tabs = mf.next().strip().split('\t')
            alpha_name = tabs.pop(0)
            alpha_names.append(alpha_name)
            p_value = tabs.pop(-1)
            p_values.append(float(p_value))
            for ind,tab in enumerate(tabs):
                group_name = group_names[ind]
                groups[group_name].alpha_mean[alpha_name] = float(tab)
    with open(total_marker,'w') as fp:
        fp.write('alpha_name\t%s\n'%'\t'.join(alpha_names))
        fp.write('p_value\t%s\n'%'\t'.join(p_values))
        for group,item in groups.iteritems():
            out_str = group
            for alpha_name in alpha_names:
                out_str += '\t%s'%item.alpha_mean[alpha_name]
            fp.write(out_str.strip() + '\n')

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(params['out_dir']):
        os.mkdir(params['out_dir'])
    marker_files = []
    for alpha_name in params['alpha_metrics'].split(','):
        file = '%s/%s.txt'%(params['alpha_dir'],alpha_name)
        marker_file = '%s/%s.marker.txt'%(params['out_dir'],alpha_name)
        vars = {'grouped_file':file,
                'marker_file':marker_file,
                'alpha_name':alpha_name}
        r_job = rp.RParser()
        r_job.open(this_script_path + '/../src/template/04_alpha_diff_test.Rtp')
        r_job.format(vars)
        r_job.write(params['out_dir'] + '/alpha_diff_boxplot.R')
        r_job.run()
        marker_files.append(marker_file)
    total_marker = params['out_dir'] + '/alpha_markers.xls'
    write(marker_files,total_marker)
