#!/usr/bin/env python
# -*- coding:utf-8 -*- #

from __future__ import division
import sys
import argparse
import os
from util import mkdir

# TODO: rewrite this script with mafft
def read_params(args):
    parser = argparse.ArgumentParser(description='''make tree wrapper | v1.0 at 2015/10/14 by liangzb ''')
    parser.add_argument('--align_seq_py', dest='align_seqs_soft', metavar='FILE', type=str, default=None,
                        help="set the align_set.py in qiime, [default find in env]")
    parser.add_argument('--filter_alignment_py', dest='filter_alignment_soft', metavar='FILE', type=str,
                        default=None,
                        help="set the filter_alignment.py in qiime, [default find in env]")
    parser.add_argument('--make_phylogeny_py', dest='make_phylogeny_soft', metavar='FILE', type=str,
                        default='make_phylogeny.py',
                        help="set the make_phylogeny.py in qiime, [default find in env]")
    parser.add_argument('-i', '--rep_set', dest='rep_set', metavar='FILE', type=str, required=True,
                        help="set the rep_set.fasta")
    parser.add_argument('-d', '--data_type', dest='data_type', metavar='16S/ITS', choices=['16S', 'ITS'], type=str,
                        default='16S',
                        help="set the data_type, must be 16S or ITS, [ default is 16S ]")
    parser.add_argument('-a', '--align_method', dest='align_method', metavar='STR', type=str, default=None,
                        help="set the align method, [default 16S:pynast, ITS:muscle]")
    parser.add_argument('-t', '--pre_align', dest='pre_align', metavar='FILE', type=str, default=None,
                        help="set the pre align, when align method is pynast this param is required")
    parser.add_argument('-m', '--lanemask', dest='lanemask', metavar='FILE', type=str, default=None,
                        help="set the lanemask file if needed")
    parser.add_argument('-o', '--out_dir', dest='out_dir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    parser.add_argument('--tree_file', dest='tree_file', metavar='FILE', type=str, default=None,
                        help="set the output tree_file [default is out_dir/rep_phylo.tre]")
    parser.add_argument('--retree',dest='retree',metavar="NUM", type=int,default=None,
                        help="mafft retree option [default is 2]")
    parser.add_argument('--mafft',dest='mafft',metavar='FILE',type=str,
                        default='/data_center_03/USER/huangy/soft/mafft-7.245-without-extensions/bin/mafft',
                        help='mafft software url [default is /data_center_03/USER/huangy/soft/mafft-7.245-without-extensions/bin/mafft]')

    args = parser.parse_args()
    params = vars(args)
    if params['align_method'] is None:
        if params['data_type'] == '16S':
            params['align_method'] = 'pynast'
        elif params['data_type'] == 'ITS':
            params['align_method'] = 'muscle'
    if params['align_method'] == 'pynast' and params['pre_align'] is None:
        parser.print_help()
        sys.exit()
    if params['tree_file'] is None:
        params['tree_file'] = params['out_dir'] + '/rep_phylo.tre'
    if params['retree'] is None:
        params['retree'] =2
    if params['mafft'] is None:
        params['mafft'] = '/data_center_03/USER/huangy/soft/mafft-7.245-without-extensions/bin/mafft'
    return params


if __name__ == '__main__':
    params = read_params(sys.argv)
    if params['data_type'] == '16S':
        mkdir(params['out_dir'])
        align_dir = '%s/align_result' % params['out_dir']
        align_file_name = os.path.splitext(os.path.basename(params['rep_set']))[0]
        align_result = '%s/%s_aligned.fasta' % (align_dir, align_file_name)
        command = '%s -i %s -m %s ' % (params['align_seqs_soft'], params['rep_set'], params['align_method'])
        if params['align_method'] == 'pynast':
            command += '-t %s ' % params['pre_align']
        command += '-o %s/align_result\n' % params['out_dir']
        if params['lanemask'] is not None:
            command += '%s -i %s -m %s -o %s\n' % (params['filter_alignment_soft'],
                                                   align_result,
                                                   params['lanemask'],
                                                   align_dir)
            align_result = os.path.splitext(align_result)[0] + '_pfiltered.fasta'
        command += '%s -i %s -o %s\n' % (params['make_phylogeny_soft'],
                                         align_result,
                                         params['tree_file'])
    elif params['data_type'] == 'ITS':
        mkdir('%s/align_result/' % params['out_dir'])
        align_result = '%s/align_result/rep_set_aligned.fasta' % params['out_dir']
        command = "%s --retree %s --progress %s  --reorder %s > " % (params['mafft'],params['retree'],"%s/stderr" % os.path.dirname(params['rep_set']),params['rep_set'])
        command += '%s\n' % align_result
        command += '%s -i %s -o %s\n' % (params['make_phylogeny_soft'],
                                         align_result,
                                         params['tree_file'])

    with open(params['out_dir'] + '/commands.sh', 'w') as fp:
        fp.write(command)
    os.system(command)
