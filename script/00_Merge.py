#!/usr/bin/env python
# -*- coding: utf-8 -*- \#

import sys
import argparse
import os
from util import mkdir, image_trans

this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
import Merge as mg
import Parser as rp


def read_params(args):
    parser = argparse.ArgumentParser(description='''16S/ITS data merge | v1.0 at 2015/09/16 by liangzb ''')
    parser.add_argument('infile_list', metavar='INFILE_LIST', nargs='+', type=str,
                        help="set your infile(s)")
    parser.add_argument('outdir', metavar='OUT_DIR', type=str, default='./',
                        help="set your output dir, default is [ PWD ], R works will be done in this dir")
    parser.add_argument('-u', '--upload_dir', dest='upload_dir', metavar='UPLOAD_DIR', type=str, default=None,
                        help="set the upload dir, [ default OUTDIR/upload ]")
    parser.add_argument('-d', '--data_type', dest='data_type', metavar='16S/ITS', choices=['16S', 'ITS'], default='16S',
                        help="set the data type, must be 16S or ITS, it is only used for the default outfile names, "
                             "[ default is 16S ]")
    parser.add_argument('-f', '--out_fasta_file', dest='out_fasta_file', metavar='FILE', type=str, default=None,
                        help="set the out_fasta_file, [ default OUTDIR/DATA_TYPE_togethr.fna ]")
    parser.add_argument('-s', '--out_stat_file', dest='out_stat_file', metavar='FILE', type=str, default=None,
                        help="set the out_stat_file, [ default OUTDIR/DATA_TYPE_together.stat ]")
    parser.add_argument('-l', '--length_stat_file', dest='length_stat_file', metavar='FILE', type=str, default=None,
                        help="set the out_length_file, [ default OUTDIR/reads_length.tsv ]")
    parser.add_argument('-o', '--upload_stat', dest='upload_stat', metavar='FILE', type=str, default=None,
                        help="set the upload stat file, [ default OUTDIR/reads_stat.tsv ]")
    parser.add_argument('--max', dest='max_length', metavar='INT', type=int, default=500,
                        help="set the max length to stat, [ default is 500 ]")
    parser.add_argument('--min', dest='min_length', metavar='INT', type=int, default=220,
                        help="set the min length to stat, [ default is 220 ]")
    parser.add_argument('--step', dest='length_step', metavar='INT', type=int, default=20,
                        help="set the length step to stat, [ default is 20 ]")
    parser.add_argument('-r', dest='required', metavar='INT', type=int, default=50000,
                        help="set the required data of this subject, [ default is 50000 ]")
    parser.add_argument('-n', dest='name_table', metavar='FILE', type=str, default=None,
                        help="set the name convert table, [ default is None ]")

    args = parser.parse_args()
    params = vars(args)
    if params['upload_dir'] is None:
        params['upload_dir'] = params['outdir'] + '/upload'
    if params['out_fasta_file'] is None:
        params['out_fasta_file'] = params['outdir'] + '/%s_together.fna' % params['data_type']
    if params['out_stat_file'] is None:
        params['out_stat_file'] = params['outdir'] + '/%s_together.stat' % params['data_type']
    if params['length_stat_file'] is None:
        params['length_stat_file'] = params['outdir'] + '/reads_length.tsv'
    if params['upload_stat'] is None:
        params['upload_stat'] = params['outdir'] + '/reads_stat.tsv'
    return params


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['upload_dir'])

    subject = mg.Subject(infile_list=params['infile_list'],
                         upload_dir=params['upload_dir'],
                         out_fasta_file=params['out_fasta_file'],
                         out_stat_file=params['out_stat_file'],
                         upload_stat=params['upload_stat'],
                         required_data=params['required'],
                         out_length_file=params['length_stat_file'],
                         max_length=params['max_length'],
                         min_length=params['min_length'],
                         length_step=params['length_step'],
                         name_table_file=params['name_table'])
    subject.read_name_table()
    subject.merge()
    subject.write_stat()
    subject.upload_stat()
    subject.write_length()

    # R works
    r_job = rp.Rparser()
    r_job.open(this_script_path + '/../src/template/00_sum_length.Rtp')
    vars = {'pdf_out': params['outdir'] + '/length_distrubution.pdf',
            'length_stat': params['length_stat_file'],
            }
    r_job.format(vars)
    r_job.write(params['outdir'] + '/length_distrubution.R')
    r_job.run()
    image_trans(params['outdir'] + '/length_distrubution.pdf', params['outdir'] + '/length_distrubution.png')
