#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import division
import sys
import argparse
import os
from util import mkdir

this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
import Parser as rp


def read_params(args):
    parser = argparse.ArgumentParser(description='''beta mrpp | v1.0 at 2016/01/05 by liangzb ''')
    parser.add_argument('-d', '--beta_div_dir', dest='beta_dir', metavar='DIR', type=str, required=True,
                        help="set the beta div dir, produced by beta_diversity.py")
    parser.add_argument('-g', '--group_file', dest='group_file', metavar='FILE', type=str, required=True,
                        help="set the group file")
    parser.add_argument('-o', '--out_dir', dest='out_dir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    args = parser.parse_args()
    params = vars(args)
    return params


def get_file_name(dir, name):
    return os.popen('ls %s/%s*.txt' % (dir, name)).read().rstrip()


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['out_dir'])
    r_job = rp.Rparser()
    r_job.open(this_script_path + '/../src/template/04_beta_mrpp.Rtp')
    file_weighted = get_file_name(params['beta_dir'], 'weighted_unifrac')
    file_unweighted = get_file_name(params['beta_dir'], 'unweighted_unifrac')
    file_out = '%s/mrpp.tsv' % params['out_dir']
    file_R = '%s/mrpp.R' % params['out_dir']

    vars_in = {
        'weighted_unifrac': file_weighted,
        'unweighted_unifrac': file_unweighted,
        'group_file': params['group_file'],
        'outfile': file_out,
    }

    r_job.format(vars_in)
    r_job.write(file_R)
    r_job.run()
