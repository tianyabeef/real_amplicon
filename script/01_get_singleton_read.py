#!/usr/bin/env python
from __future__ import division
import sys
import os
import argparse
from util import mkdir
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/../src')
import GetSingleton as gs

def read_params(args):
    parser = argparse.ArgumentParser(description='get singleton reads | v1.0 at 2015/09/16 by liangzb')
    parser.add_argument('-i','--infile',dest='infile',metavar='FILE',type=str,required=True,
            help="set the input file")
    parser.add_argument('-o','--outdir',dest='outdir',metavar='OUTDIR',type=str,default='./single',
            help="set the output dir, [ default is PWD/single ]")
    parser.add_argument('-f','--out_fa',dest='outfa',metavar='FILE',type=str,default=None,
            help="set the output fasta file, [ default is OUTDIR/derep.fa ]")
    parser.add_argument('-s','--out_stat',dest='outstat',metavar='FILE',type=str,default=None,
            help="set the output stat file, [ default is OUTDIR/stat.txt ]")
    parser.add_argument('--single_list',dest='single_list',metavar='FILE',type=str,default=None,
            help="set the single read list file, [ default is OUTDIR/single.list ]")

    args = parser.parse_args()
    params = vars(args)
    if params['outfa'] is None:
        params['outfa'] = params['outdir'] + '/derep.fa'
    if params['outstat'] is None:
        params['outstat'] = params['outdir'] + '/stat.txt'
    if params['single_list'] is None:
        params['single_list'] = params['outdir'] + '/single.list'
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['outdir'])
    subject = gs.Subject(params['infile'],params['outfa'],params['outstat'],params['single_list'])
    subject.find_record()
    subject.write_fa()
    subject.write_stat()

