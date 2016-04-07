#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

import argparse
import sys
import os
import re
import pandas as pd
from util import mkdir
def read_params(args):
    parser = argparse.ArgumentParser(description='''diff pca | v1.0 at 2015/10/26 by liangzb ''')
    parser.add_argument('-i', '--infile', dest='infile', metavar='file', type=str, required=True,
                        help="set the marker file in")
    parser.add_argument('-g', '--group', dest='group', metavar='file', type=str, default=None,
                        help="set group file")
    parser.add_argument('-o', '--outdir', dest='outdir', metavar='DIR', type=str, required=True,
                        help="set the work dir")
    parser.add_argument('--cut_off', dest='cut_off', metavar='cut_off', type=float, required=True,
                        help="set the  cut off abundance")
    parser.add_argument('--quantile', dest='quantile', metavar='quantile', type=float, default=1.0,
                        help="thr sum of raw  set quantile;0.25 or 0.5 or 0.75")
    args = parser.parse_args()
    params = vars(args)
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    group = params["group"]
    infile = params['infile']
    outdir = params['outdir']
    cut_off = params['cut_off']
    quantile = params['quantile']
    basename = os.path.basename(infile)
    prefix = os.path.splitext(basename)
    tmp_file = "%s/%s_tmp"% (outdir,basename)
    if not os.path.exists(outdir):
        mkdir(outdir)
    with open(infile) as fq, open(tmp_file, 'w') as out:
        head = fq.next()
        if head.startswith('# Constructed from'):
            head = fq.next()
        out.write(head)
        for line in fq:
            tabs = line.strip().split("\t")
            if tabs[0].split(";")[-1]=="Other":
                    continue
#            tabs[0]=tabs[0].split(";")[-1]
#            out.write("%s\n" % "\t".join(tabs))
            out.write(line)
    df = pd.DataFrame.from_csv(tmp_file,sep="\t")
    if group is not None:
	dfgroup=[]
	with open(group,"r") as fq:
	    for line in fq:
		tabs = line.strip().split("\t")
		dfgroup.append(tabs[0])
        df = df[dfgroup]
    sample_num = len(df.columns)
    df["sum"] = df.sum(axis=1)
    df = df.sort("sum",ascending=False)
    quantile_value = float(df["sum"].quantile(quantile))
    dd = df[df>cut_off]
    df["num_True"] = dd.count(axis=1)
    index_list = []
    for i in range(len(df.index)):
        if df.ix[i,sample_num] < quantile_value:
            if df.ix[i,sample_num+1] <2:
                index_list.append(i)
    df = df.drop(df.index[index_list])
    del df["sum"]
    del df["num_True"]
    df.to_csv("%s/%s"% (outdir,basename),sep="\t",encoding="utf-8")
    os.popen("rm %s" % tmp_file)

