#!/usr/bin/env python
from __future__ import division
import sys
import os
import re
import argparse

def read_params(args):
    parser = argparse.ArgumentParser(description='a wrapper for rdp classify | v1.0 at 2015/09/18 by liangzb')
    parser.add_argument('-j','--jar',dest='jar',metavar='JAR',type=str,required=True,
            help="set the classifier.jar with absolute path")
    parser.add_argument('-i','--infile',dest='infile',metavar='FILE',type=str,required=True,
            help="set the input fasta file to classify")
    parser.add_argument('-d','--data_type',dest='data_type',metavar='16S/ITS',choices=['16S','ITS'],type=str,default='16S',
            help="set the data_type, must be 16S or ITS, [ default is 16S ]")
    parser.add_argument('-o','--output',dest='outfile',metavar='FILE',type=str,required=True,
            help="set the output file, which is tab-delimited text for classification")
    parser.add_argument('-c','--conf',dest='conf',metavar='FLOAT',type=float,default=0.8,
            help="set the confidence cutoff, range [0-1], [ default is 0.8 ]")
    parser.add_argument('--hier_outfile',dest='hierfile',metavar='FILE',type=str,default=None,
            help="set the out hier file, which containing the assignment count for each taxon in the hierarchical format")

    args = parser.parse_args()
    params = vars(args)
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(os.path.dirname(params['outfile'])):
        os.mkdir(os.path.dirname(params['outfile']))
    if params['hierfile'] and not os.path.isdir(os.path.dirname(params['hierfile'])):
        print params['hierfile']
        print not os.path.isdir(os.path.dirname(params['hierfile']))
        os.mkdir(os.path.dirname(params['hierfile']))

    commands = 'java -Xmx1g -jar %s classify '%params['jar']
    if params['data_type'] == '16S':
        commands += ' -g 16srrna '
    elif params['data_type'] == 'ITS':
        commands += ' -g fungalits_unite '
    commands += ' -c %s -o %s'%(params['conf'],params['outfile'])
    if params['hierfile']:
        commands += ' -h %s '%params['hierfile']
    commands += params['infile']

    os.system(commands)

