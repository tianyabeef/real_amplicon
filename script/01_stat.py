#!/usr/bin/env python
from __future__ import division
import sys
import os
import argparse
from util import mkdir

this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
import PickOtuStat as ps


def read_params(args):
    parser = argparse.ArgumentParser(description='summary stat from previous stats | v1.0 at 2015/09/16 by liangzb',
                                     epilog='you must set at least one of --uc or --otutab, if you set both, --uc used')
    parser.add_argument('-r', dest='raw_data_stat', metavar='FILE', type=str, required=True,
                        help="set the data stat file produced by 00_Merge.py ")
    parser.add_argument('-s', dest='single_stat', metavar='FILE', type=str, required=True,
                        help="set the single stat file produced by 01_get_singleton_read.py")
    parser.add_argument('--uc', dest='uc_file', metavar='FILE', type=str, default=None,
                        help="set the uc file to get mapped reads, must be set when leave otutab file free")
    parser.add_argument('--otutab', dest='otutab', metavar='FILE', type=str, default=None,
                        help="set the otutab file to get mapped reads, must be set when leave uc file free")
    parser.add_argument('--single_list', dest='single_list', metavar='FILE', type=str, default=None,
                        help="set the single list file produced by 01_get_single_read")
    parser.add_argument('-o', dest='outfile', metavar='FILE', type=str, required=True,
                        help="set the output xls file ")

    args = parser.parse_args()
    params = vars(args)
    if params['uc_file'] is None and params['otutab'] is None:
        parser.print_help()
        sys.exit()
    return params


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(os.path.dirname(params['outfile']))

    subject = ps.Subject()
    subject.read_raw_data_stat(params['raw_data_stat'])
    subject.read_single_list(params['single_list'])
    subject.read_single_stat(params['single_stat'])
    if params['uc_file']:
        subject.get_mapped_tags_from_uc(params['uc_file'])
    else:
        subject.get_mapped_tags_from_otutab(params['otutab'])
    subject.write(params['outfile'], '%s.fullstat' % params['outfile'])
