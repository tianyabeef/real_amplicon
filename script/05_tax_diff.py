#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import sys
import argparse
import os
from util import mkdir

this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
import Parser as rp


def read_params(args):
    parser = argparse.ArgumentParser(description='''tax diff | v1.0 at 2015/10/26 by liangzb ''')
    parser.add_argument('-i', '--infile', dest='infile', metavar='FILE', type=str, required=True,
                        help="set the transed file")
    parser.add_argument('-o', '--outdir', dest='outdir', metavar='DIR', type=str, required=True,
                        help="set the work dir")
    parser.add_argument('-g', '--group', dest='group', metavar='FILE', type=str, required=True,
                        help="set the group file")
    parser.add_argument('-c', '--cutoff', dest='cutoff', metavar='FILE', type=float, default=0.05,
                        help="set the p_value cutoff")
    parser.add_argument('-q', '--fdr', dest='fdr', metavar='FILE', type=float, default=0.05,
                        help="set the fdr cutoff")
    parser.add_argument('--paired', dest='paired', action='store_true',
                        help="paired compare")
    parser.set_defaults(paired=False)
    args = parser.parse_args()
    params = vars(args)
    params['marker'] = params['outdir'] + '/diff.marker.tsv'
    params['filt'] = params['outdir'] + '/diff.marker.filt.tsv'
    params['profile'] = params['outdir'] + '/profile.for_plot.txt'
    params['paired'] = judge(params['paired'])
    return params


def judge(value):
    if value:
        value = 'TRUE'
    else:
        value = 'FALSE'
    return value


def filt(infile, filt_file):
    marker_set = set()
    with open(infile) as fp, open(filt_file, 'w') as out:
        out.write(fp.next())
        for line in fp:
            tabs = line.strip().split('\t')
            try:
                p_value = float(tabs[-2])
                q_value = float(tabs[-1])
            except ValueError, ex:
                if str(ex).startswith('could not convert string to float'):
                    continue
            if p_value < params['cutoff'] and q_value < params["fdr"]:
                marker_set.add(tabs[0])
                out.write(line)
    return marker_set


def get_profile(marker_set, infile, outfile):
    with open(infile) as fp, open(outfile, 'w') as out:
        out.write(fp.next())
        for line in fp:
            name = line.split('\t')[0]
            if name in marker_set:
                out.write(line)


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['outdir'])
    r_job = rp.Rparser()
    r_job.open(this_script_path + '/../src/template/05_diff_test.Rtp')
    var = {
        'infile': params['infile'],
        'group_file': params['group'],
        'marker_file': params['marker'],
        'paired': params['paired'],
    }
    r_job.format(var)
    r_job.write(params['outdir'] + '/diff.marker.R')
    r_job.run()
    marker_set = filt(params['marker'], params['filt'])
    get_profile(marker_set, params['infile'], params['profile'])
