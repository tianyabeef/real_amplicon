#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import sys
import argparse
import os
from util import mkdir, image_trans

this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
import Parser as rp


def read_params(args):
    parser = argparse.ArgumentParser(description='''diff pca | v1.0 at 2015/10/26 by liangzb ''')
    parser.add_argument('-i', '--infile', dest='infile', metavar='file', type=str, required=True,
                        help="set the marker file in")
    parser.add_argument('-o', '--outdir', dest='outdir', metavar='DIR', type=str, required=True,
                        help="set the work dir")
    parser.add_argument('-g', '--group', dest='group', metavar='FILE', type=str, required=True,
                        help="set the group file")
    args = parser.parse_args()
    params = vars(args)
    return params


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['outdir'])
    r_job = rp.Rparser()
    r_job.open(this_script_path + '/../src/template/05_diff_pca.Rtp')
    r_file = params['outdir'] + '/diff_pca.R'
    pdf_file = params['outdir'] + '/diff_pca.pdf'
    png_file = params['outdir'] + '/diff_pca.png'
    var = {
        'input_file': params['infile'],
        'group_file': params['group'],
        'pdf_file': pdf_file
    }
    r_job.format(var)
    r_job.write(r_file)
    r_job.run()
    image_trans(pdf_file, png_file)
