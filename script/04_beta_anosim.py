#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import division
import sys
import argparse
import os
from util import mkdir, image_trans

this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
import Parser as rp


def read_params(args):
    parser = argparse.ArgumentParser(description='''beta anosim | v1.0 at 2015/12/23 by liangzb ''')
    parser.add_argument('-d', '--beta_div_dir', dest='beta_dir', metavar='DIR', type=str, required=True,
                        help="set the beta div dir, produced by beta_diversity.py")
    parser.add_argument('-g', '--group_file', dest='group_file', metavar='FILE', type=str, required=True,
                        help="set the group file")
    parser.add_argument('-o', '--out_dir', dest='out_dir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    args = parser.parse_args()
    params = vars(args)
    return params


def work(r_job, name, params):
    file_name = os.popen('ls %s/%s*.txt' % (params['beta_dir'], name)).read().strip()
    file_pdf = '%s/%s.anosim.pdf' % (params['out_dir'], name)
    file_png = '%s/%s.anosim.png' % (params['out_dir'], name)
    file_R = '%s/%s.anosim.R' % (params['out_dir'], name)
    distance_name = name.replace('_', ' ').title()
    vars_in = {'distance_table': file_name,
               'group_file': params['group_file'],
               'pdf_file': file_pdf,
               'distance_name': distance_name
               }
    r_job.format(vars_in)
    r_job.write(file_R)
    r_job.run()
    image_trans(file_pdf, file_png)


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['out_dir'])
    r_job = rp.Rparser()
    r_job.open(this_script_path + '/../src/template/04_beta_anosim.Rtp')

    for name in ['weighted_unifrac', 'unweighted_unifrac']:
        work(r_job, name, params)
