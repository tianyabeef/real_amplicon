#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import division
import sys
import argparse
import os
from util import mkdir,image_trans
this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
import Parser as rp

def read_params(args):
    parser = argparse.ArgumentParser(description='''beta pcoa | v1.0 at 2015/10/16 by liangzb ''')
    parser.add_argument('-d','--beta_div_dir',dest='beta_dir',metavar='DIR',type=str,required=True,
                        help="set the beta div dir, produced by beta_diversity.py")
    parser.add_argument('-g','--group_file',dest='group_file',metavar='FILE',type=str,required=True,
                        help="set the group file")
    parser.add_argument('-o', '--out_dir', dest='out_dir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    parser.add_argument('-w', '--with_boxplot', dest='with_boxplot', metavar='BOOL', type=bool, default=True,
                        help="set the param 'False' to disable boxplot, [default is True]")
    args = parser.parse_args()
    params = vars(args)
    return params

def work(r_job,name,params):
    file = os.popen('ls %s/%s*.txt'%(params['beta_dir'],name)).read().strip()
    pdf_file = '%s/%s.pcoa.pdf'%(params['out_dir'],name)
    png_file = '%s/%s.pcoa.png'%(params['out_dir'],name)
    R_file = '%s/%s.pcoa.R'%(params['out_dir'],name)
    distance_name = name.replace('_',' ').title()
    vars = {'distance_table':file,
            'group_file':params['group_file'],
            'pdf_file':pdf_file,
            'distance_name':distance_name}
    r_job.format(vars)
    r_job.write(R_file)
    r_job.run()
    image_trans(pdf_file,png_file)

if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['out_dir'])
    r_job = rp.Rparser()
    if params['with_boxplot']:
        r_job.open(this_script_path + '/../src/template/04_beta_pcoa_with_boxplot.Rtp')
    else:
        r_job.open(this_script_path + '/../src/template/04_beta_pcoa.Rtp')

    for name in ['weighted_unifrac','unweighted_unifrac']:
        work(r_job,name,params)
