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
    parser.add_argument('--cut_off', dest='cut_off', metavar='cut_off', type=int, required=True,
                        help="set the group file")
    parser.add_argument('--quantile', dest='quantile', metavar='quantile', type=float, default=0.25,
                        help="thr sum of raw  set quantile;0.25 or 0.5 or 0.75")
    args = parser.parse_args()
    params = vars(args)
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    infile = params['infile']
    outdir = params['outdir']
    cut_off = params['cut_off']
    quantile = params['quantile']
    if os.path.isfile(infile):
        basename = os.path.basename(infile)
        prefix = os.path.splitext(basename)
        df = pd.DataFrame.from_csv(infile,sep="\t")
        sample_num = len(df.columns)
        df["sum"] = df.sum(axis=1)
        df = df.sort("sum",ascending=False)
        quantile_value = df["sum"].quantile(quantile)
        dd = df[df>cut_off]
        df["num_True"] = dd.count(axis=1)
        for i in range(len(df.index)):
            if df.icol[i,sample_num+1] < quantile_value:
                if df.icol[i,sample_num+2] < sample_num:
                    df.drop(df.index[i])
        del df["sum"]
        del df["num_True"]
        df.to_csv("%s/%s"% (outdir,basename),sep="\t",encoding="utf-8")

