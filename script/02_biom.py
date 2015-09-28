#!/usr/bin/env python
from __future__ import division
import sys
import os
import re
import argparse

def read_params(args):
    parser = argparse.ArgumentParser(description='a wrapper for biom | v1.0 at 2015/09/28 by liangzb')
    parser.add_argument('-s','--biom_soft',dest='biom',metavar='BIOM',type=str,required=True,
            help="set the biom software with absolute path")
    parser.add_argument('-i','--biom_file',dest='biomfile',metavar='FILE',type=str,required=True,
            help="set the input biom file")
    parser.add_argument('-o','--out_file',dest='outfile',metavar='FILE',type=str,required=True,
            help="set the output txt file")

    args = parser.parse_args()
    params = vars(args)
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(os.path.dirname(params['outfile'])):
        os.mkdir(os.path.dirname(params['outfile']))
    basename,suffix = os.path.splitext(params['outfile'])
    params['summary'] = basename + '_summary' + suffix

    if os.path.isfile(params['summary']):
        os.remove(params['summary'])
    if os.path.isfile(params['outfile']):
        os.remove(params['outfile'])

    os.system('%s summarize-table -i %s -o %s'%(params['biom'],
                                                params['biomfile'],
                                                params['summary']))
    os.system('%s convert -i %s -o %s --to-tsv'%(params['biom'],
                                                 params['biomfile'],
                                                 params['outfile']))


