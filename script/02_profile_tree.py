#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import division
import sys
import os
import argparse
from util import mkdir
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/../src')
from SumProfileTree import Subject


def read_params(args):
    parser = argparse.ArgumentParser(description='make profile tree file | v1.0 at 2015/10/21 by liangzb')
    parser.add_argument('-t','--tax_ass',dest='tax_ass',metavar='FILE',type=str,required=True,
                        help="set the tax_assignment file")
    parser.add_argument('-i','--otu_table',dest='otu_table',metavar='FILE',type=str,required=True,
                        help="set the otu profile table")
    parser.add_argument('-o','--out_file',dest='out_file',metavar='FILE',type=str,required=True,
                        help="set the output file")
    parser.add_argument('-g','--group',dest='group',metavar='FILE',type=str,default=None,
                        help="if set the group, outfile will be written with group")
    parser.add_argument('-e','--expand',dest='expand',metavar='INT',type=int,default=1,
                        help="expand the total profile, [default is 1]")
    args = parser.parse_args()
    params = vars(args)
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(os.path.dirname(params['out_file']))
    subject = Subject(params['otu_table'],params['tax_ass'],params['out_file'],group_file=params['group'],expand=params['expand'])
    subject.work()
