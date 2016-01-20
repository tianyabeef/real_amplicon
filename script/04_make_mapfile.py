#!/usr/bin/env python
# -*- coding: utf-8 -*- \#


import sys
import argparse
import os
from util import mkdir

this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
from Parser import parse_group_file


def read_params(args):
    parser = argparse.ArgumentParser(description='''make mapfile by group files | v1.0 at 2015/11/2 by liangzb ''')
    parser.add_argument('-g', '--group_list', dest='group_list', metavar='FILE_LIST', nargs='+', type=str,
                        required=True,
                        help="set the group file list")
    parser.add_argument('-o', '--outfile', dest='outfile', metavar='FILE', type=str, required=True,
                        help="set the output mapfile")

    args = parser.parse_args()
    params = vars(args)
    return params


def work(sample_list, group_dict, outfile):
    with open(outfile, 'w') as out:
        group_names = sorted(list(group_dict.iterkeys()))
        out.write('#SampleID\t%s\n' % '\t'.join(group_names))
        for sample in sample_list:
            out_str = sample
            for group_name in group_names:
                group = group_dict[group_name]
                if sample not in group:
                    group[sample] = ''
                out_str += '\t%s' % group[sample]
            out.write(out_str.strip() + '\n')


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(os.path.dirname(params['outfile']))
    sample_list = []
    group_dict = {}
    for group_file in params['group_list']:
        group_name = os.path.basename(group_file)
        group_name = os.path.splitext(group_name)[0]
        group = parse_group_file(group_file)
        group_dict[group_name] = group
        sample_list += list(group.iterkeys())
    sample_list = list(set(sample_list))
    work(sample_list, group_dict, params['outfile'])
