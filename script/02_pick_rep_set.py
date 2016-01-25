#!/usr/bin/env python
# -*- coding: utf-8 -*- \#
"""
@author = 'liangzb'
@date = '2016-01-25'

"""

from __future__ import division
import re
import sys
import os
import argparse
from util import mkdir

this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
from Parser import parse_group_file


def read_params(args):
    parser = argparse.ArgumentParser(description='a wrapper for rdp classify | v1.0 at 2015/09/18 by liangzb')
    parser.add_argument('--pick_rep_set', dest='pick_rep_set', metavar='FILE', type=str, default='pick_rep_set.py',
                        help="set the pick_rep_set.py of qiime, [default find in env]")
    parser.add_argument('-i', '--otu_mapping_file', dest='otu_mapping', metavar='FILE', type=str, required=True,
                        help="set the otu mapping file")
    parser.add_argument('-f', '--fasta_file', dest='reference_seqs', metavar='FILE', type=str, required=True,
                        help="set the fasta file")
    parser.add_argument('-m', '--picking_method', dest='picking_method', metavar='STR', choices=['first',
                                                                                                 'random',
                                                                                                 'longest',
                                                                                                 'most_abundant'],
                        type=str, default='most_abundant',
                        help="set the picking method, choice from: first, random, longest, most_abundant, \
                              [default is most_abundant]")
    parser.add_argument('-g', '--group', dest='group', metavar='FILE', type=str, default=None,
                        help="set the group file, if is setted, \
                             rep set will pick each group with a prefix of group_name")
    parser.add_argument('-o', '--outdir', dest='outdir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    args = parser.parse_args()
    params = vars(args)
    if params['group']:
        params['group'] = parse_group_file(params['group'])
    else:
        params['group'] = None
    return params


def work_with_group(otu_mapping, outfile, group_name):
    reg = re.compile(r'(\S+)_\d+$')
    with open(otu_mapping) as fp, open(outfile, 'w') as out:
        for line in fp:
            tabs = line.rstrip().split('\t')
            filtered_list = []
            for seq_id in tabs[1:]:
                sample_name = reg.search(seq_id).group(1)
                if params['group'][sample_name] == group_name:
                    filtered_list.append(seq_id)
            if filtered_list:
                out.write('%s\t%s\n' % (tabs[0], '\t'.join(filtered_list)))


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['outdir'])
    commands_file = '%s/commands.sh' % params['outdir']
    commands = []
    if params['group'] is not None:
        group_names = set(params['group'].itervalues())
        for group_name in group_names:
            out_otu_mapping = '%s/%s.otu_mapping' % (params['outdir'], group_name)
            outfile = '%s/%s.rep_set.fna' % (params['outdir'], group_name)
            work_with_group(params['otu_mapping'], out_otu_mapping, group_name)
            commands.append('%s -i %s -f %s -o %s -m %s' % (params['pick_rep_set'],
                                                            out_otu_mapping,
                                                            params['reference_seqs'],
                                                            outfile,
                                                            params['picking_method']))
    else:
        outfile = '%s/rep_set.fna' % params['outdir']
        commands.append('%s -i %s -f %s -o %s -m %s' % (params['pick_rep_set'],
                                                        params['otu_mapping'],
                                                        params['reference_seqs'],
                                                        outfile,
                                                        params['picking_method']))
    with open(commands_file, 'w') as out:
        out.write('\n'.join(commands))
    for command in commands:
        os.system(command)
