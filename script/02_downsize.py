#!/usr/bin/env python
import sys
import argparse
import os
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/../src')
from Downsize import Subject


def read_params(args):
    parser = argparse.ArgumentParser(description='''downsize script | v1.0 at 2015/09/28 by liangzb ''')
    parser.add_argument('-m','--minimum',dest='minimum',metavar='INT',type=int,default=None,
            help="set the minimum to downsize, [default is None]")
    parser.add_argument('-s','--in_statfile',dest='statfile',metavar='INT',type=str,default=None,
            help="find the minimum from statfile which produced by 01_stat, can be overrited by MINIMUM")
    parser.add_argument('-i','--otu_table',dest='otu_table',metavar='STR',type=str,required=True,
            help="set the otu_table")
    parser.add_argument('-o','--outfile',dest='outfile',metavar='OUTFILE',type=str,required=True,
            help="set the output file")
    parser.add_argument('--out_statfile',dest='outstatfile',metavar='FILE',type=str,default=None,
            help="set the stat file")
    parser.add_argument('-k','--keep_small_size',dest='keep',metavar='BOOL',type=bool,default=True,
            help="if keep the small size, [default is True]")
    parser.add_argument('-r','--random',dest='random',metavar='BOOL',type=bool,default=True,
            help="if downsize random, [default is True]")
    parser.add_argument('-g','--group',dest='group',metavar='FILE',type=str,default=None,
            help="if set the group file, in_stat_file will be overwrited")

    args = parser.parse_args()
    params = vars(args)
    if params['minimum'] is None and params['statfile'] is None:
        parser.print_help()
        sys.exit()
    if params['minimum'] is None and params['statfile'] is not None:
        params['minimum'] = find_minimum(params['statfile'],params['group'])
    return params

def find_minimum(file,group):
    sample_set = set()
    if group is not None:
        with open(group) as group:
            for line in group:
                sample.add(line.split('\t')[0])

    with open(file) as fp:
        line = fp.next()
        while(line):
            line = fp.next().strip()
        header = fp.next()
        minimum = 0xffffff
        for line in fp:
            tabs = line.split('\t')
            if sample_set and tabs[0] not in sample_set:
                continue
            n = int(tabs[2])
            if n < minimum:
                minimum = n
    return minimum

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(os.path.dirname(params['outfile'])):
        os.mkdir(os.path.dirname(params['outfile']))
    s = Subject(params['otu_table'],params['outfile'],params['outstatfile'],params['minimum'],params['keep'],params['random'])
    s.work()

