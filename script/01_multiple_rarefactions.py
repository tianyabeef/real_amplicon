#!/usr/bin/env python
from __future__ import division
import sys
import os
import re
import argparse
from skbio.stats import subsample

this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/../src')
from MyRarefactionMaker import MyRarefactionMaker

def read_params(args):
    parser = argparse.ArgumentParser(description='multiple_rarefactions | v1.0 at 2015/09/21 by liangzb')
    parser.add_argument('-r','--multiple_rarefactions',dest='multiple_rarefactions',metavar='STR',default='multiple_rarefactions.py',
            help="set the path of multiple_rarefactions.py, default will find in PATH")
    parser.add_argument('-i','--infile',dest='infile',metavar='FILE',type=str,required=True,
            help="set the input biom file")
    parser.add_argument('-o','--outdir',dest='outdir',metavar='OUTDIR',type=str,default='./rarefaction',
            help="set the output dir, [default is PWD/rarefaction ]")
    parser.add_argument('-m','--min',dest='min',metavar='INT',type=int,default=10,
            help="minimum of seqs for rarefaction, [default is 10]")
    parser.add_argument('-s','--step',dest='step',metavar='INT',type=int,default=4000,
            help="size of steps between min/max, [default is 4000]")
    parser.add_argument('-x','--max',dest='max',metavar='INT',type=int,
            help="maximum of seqs for rarefaction, make sure that at least one sample's seq num must over this number\
                  it can be overrited by STATFILE")
    parser.add_argument('-t','--statfile',dest='statfile',metavar='FILE',type=str,default=None,
            help="set the statfile produced by 01_stat.py")

    args = parser.parse_args()
    params = vars(args)
    if params['statfile'] is not None:
        params['max'] = get_maximum(params['statfile'])
    if params['max'] is None and params['statfile'] is None:
        parser.print_help()
        sys.exit()
    return params

def get_maximum(file):
    fp = open(file)
    line = fp.next()
    while(line):
        line = fp.next().strip()
    head = fp.next()
    maximum = max([int(line.strip().split('\t')[2]) for line in fp])
    fp.close()
    return maximum

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(params['outdir']):
        os.mkdir(params['outdir'])


    __range = []
    if range(params['max'] > 10000):
        __range += range(params['min'],10000,int(params['step'] / 10)) + range(10000,params['max'],params['step']) 
    else:
        __range = range(params['min'],params['max'],params['step'])

    maker = MyRarefactionMaker(params['infile'],__range,10)

    maker.rarefy_to_files(params['outdir'],
                          False,
                          False,
                          True,
                          subsample)
