#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

import argparse
import sys
import os
import pandas as pd
def read_params(args):
    parser = argparse.ArgumentParser(description='''diff pca | v1.0 at 2015/10/26 by liangzb ''')
    parser.add_argument('-i', '--infile', dest='infile', metavar='file', type=str, required=True,
                        help="set the marker file in")
    parser.add_argument('-o', '--outdir', dest='outdir', metavar='DIR', type=str, required=True,
                        help="set the work dir")
    parser.add_argument('-g', '--group', dest='group', metavar='FILE', type=str, required=True,
                        help="set the group file")
    parser.add_argument('--cut_off', dest='cut_off', metavar='cut_off', type=int, required=True,
                        help="set the group file")
    args = parser.parse_args()
    params = vars(args)
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    infile = params['infile']
    outdir = params['outdir']
    group = params['group']
    cut_off = params['cut_off']
    if os.path.isfile(infile):
        df = pd.DataFrame.from_csv(infile,sep="\t")
        df["sum"] = df.sum(axis=1)
        df = df.sort("sum",ascending=False)
        abundance_sum = df.sum()[-1]
        dd = df[df>cut_off]
        df["num_True"] = dd.count(axis=1)
        for i in range(100):
            df.icol[i,18] > 18