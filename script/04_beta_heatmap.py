#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import division
import sys
import argparse
import os
this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
import Parser as rp

def read_params(args):
    parser = argparse.ArgumentParser(description='''beta heatmap | v1.0 at 2015/10/16 by liangzb ''')
    parser.add_argument('-d','--beta_div_dir',dest='beta_dir',metavar='DIR',type=str,required=True,
                        help="set the beta div dir, produced by beta_diversity.py")
    parser.add_argument('-g','--group_file',dest='group_file',metavar='FILE',type=str,required=True,
                        help="set the group file")
    parser.add_argument('-o', '--out_dir', dest='out_dir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    args = parser.parse_args()
    params = vars(args)
    return params

def work(r_job,name,params):
    file = os.popen('ls %s/%s*.txt'%(params['beta_dir'],name)).read().strip()
    pdf_file = '%s/%s.heatmap.pdf'%(params['out_dir'],name)
    png_file = '%s/%s.heatmap.png'%(params['out_dir'],name)
    R_file = '%s/%s.heatmap.R'%(params['out_dir'],name)
    distance_name = name.replace('_',' ').title()
    vars = {'for_plot':file,
            'group_file':params['group_file'],
            'pdf_file':pdf_file,
            'distance_name':distance_name}
    r_job.format(vars)
    r_job.write(R_file)
    r_job.run()
    os.system('convert %s %s'%(pdf_file,png_file))

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(params['out_dir']):
        os.mkdir(params['out_dir'])
    r_job = rp.Parser()
    r_job.open(this_script_path + '/../src/template/04_beta_heatmap.Rtp')

    for name in ['weighted_unifrac','unweighted_unifrac']:
        work(r_job,name,params)
