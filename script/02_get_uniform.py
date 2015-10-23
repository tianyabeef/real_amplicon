#!/usr/bin/env python
from __future__ import division
import sys
import os
import argparse
from util import mkdir
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/../src')
from Parser import TableParser


def read_params(args):
    parser = argparse.ArgumentParser(description='get otu profile uniform | v1.0 at 2015/09/29 by liangzb')
    parser.add_argument('-i','--infile',dest='infile',metavar='FILE',type=str,required=True,
            help="set the un-uniformed profile produced by biom convert")
    parser.add_argument('-o','--out_file',dest='outfile',metavar='FILE',type=str,required=True,
            help="set the output uniform profile")

    args = parser.parse_args()
    params = vars(args)
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(os.path.dirname(params['outfile']))
    table = TableParser(params['infile'])
    table.parse_table()
    table.get_uniform()
    table.write_table(params['outfile'])
