#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import division
import sys
import argparse

def read_params(args):
    parser = argparse.ArgumentParser(description='''trans summarize outfiles | v1.0 at 2015/10/19 by liangzb ''')
    parser.add_argument('-i', '--summarize_dir', dest='summarize_dir', metavar='DIR', type=str, required=True,
                        help="set the summarize_taxa outdir as input")
    parser.add_argument('--prefix', dest='prefix', metavar='STR', type=str, default='otu_table',
                        help="set the summarize taxa file prefix, [ default is otu_table ]")
    args = parser.parse_args()
    params = vars(args)
    return params

def work_trans(L2_file,L1_file):
    profile = {}
    with open(L2_file) as L2,open(L1_file,'w') as L1:
        for line in L2:
            if line.startswith('#'):
                L1.write(line)
                continue
            tabs = line.strip().split('\t')
            tax = tabs.pop(0).split(';')[0]
            if tax not in profile:
                profile[tax] = map(lambda s:float(s),tabs)
            else:
                for ind,tab in enumerate(tabs):
                    profile[tax][ind] += float(tab)
        for tax in profile:
            L1.write('%s\t%s\n'%(tax,'\t'.join(map(lambda s:str(s),profile[tax]))))

def parse_file(file):
    content = []
    with open(file) as f:
        for line in f:
            if line.startswith('# Constructed from'):
                continue
            if line.startswith('#'):
                head = line
                continue
            content.append(line.strip())
    return head,content

def merge_files(files,outfile):
    contents = []
    for file in files:
        head,content = parse_file(file)
        contents += content
    contents.sort()
    with open(outfile,'w') as out:
        out.write('%s%s\n'%(head,'\n'.join(contents)))

if __name__ == '__main__':
    params = read_params(sys.argv)
    summarize_files = ['%s/%s_L%d.txt'%(params['summarize_dir'],params['prefix'],i) for i in range(1,6)]
    work_trans(summarize_files[1],summarize_files[0])
    merged_file = '%s/%s_all.txt'%(params['summarize_dir'],params['prefix'])
    merge_files(summarize_files,merged_file)
