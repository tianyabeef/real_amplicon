#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import sys
import os
import re
import argparse
from util import mkdir
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/../src')

def read_params(args):
    parser = argparse.ArgumentParser(description='trans_profile | v1.0 at 2015/10/19 by liangzb')
    parser.add_argument('-i','--infile',dest='infile',metavar='FILE',type=str,required=True,
                        help="set the input file")
    parser.add_argument('-o','--outfile',dest='outfile',metavar='FILE',type=str,required=True,
                        help="set the output file")
    parser.add_argument('-m','--mode',dest='mode',metavar='STR',choices=['all','phylum','class','order','family','genus','species','otu'],required=True,
                        help="set the file mode,should be one of: all,phylum,class,order,family,genus,species or otu")
    args = parser.parse_args()
    params = vars(args)
    return params

def trans(infile,outfile,level=None):
    with open(infile) as fp,open(outfile,'w') as out:
        head = fp.next()
        if head.startswith('# Constructed from'):
            head = fp.next()
        out.write(head.lstrip('#'))
        profiles = {}
        for line in fp:
            tabs = line.strip().split('\t')
            taxes = tabs[0].split(';')
            for tax in taxes :
                if level is None:
                    if not re.search('\w__',tax):
                        continue
                else:
                    if not re.search('\%s__'%level,tax):
                        continue
                if tax not in profiles:
                    profiles[tax] = map(lambda a:float(a),tabs[1:])
                else:
                    profiles[tax] = map(lambda a,b:float(a)+float(b), profiles[tax],tabs[1:])
        for tax in sorted(profiles.iterkeys()):
            out.write('%s\t%s\n'%(tax,'\t'.join(map(lambda s:str(s),profiles[tax]))))

if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(os.path.dirname(params['outfile']))
    if params['mode'] == 'otu':
        os.system('copy %s %s'%(params['infile'],params['outfile']))
    elif params['mode'] == 'all':
        trans(params['infile'],params['outfile'])
    else:
        level = params['mode'].lower()[0]
        trans(params['infile'],params['outfile'],level=level)
