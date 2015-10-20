#!/usr/bin/env python
from __future__ import division
import sys
import os
import argparse
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/../src')
import Parser as rp


def read_params(args):
    parser = argparse.ArgumentParser(description='specaccum | v1.0 at 2015/10/09 by liangzb')
    parser.add_argument('-i','--otu_table',dest='otu_table',metavar='FILE',type=str,required=True,
            help="set the otu_table file, make sure there is no necessary content")
    parser.add_argument('-o','--out_dir',dest='out_dir',metavar='DIR',type=str,required=True,
            help="set the output dir which R works in")

    args = parser.parse_args()
    params = vars(args)
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(params['out_dir']):
        os.mkdir(params['out_dir'])
    pdf_file = '%s/specaccum.pdf'%params['out_dir']
    png_file = '%s/specaccum.png'%params['out_dir']
    Rscript = '%s/specaccum.R'%params['out_dir']
    r_job = rp.Rparser()
    r_job.open(this_script_path + '/../src/template/02_specaccum.Rtp')
    vars = {"otu_table":params['otu_table'],
            "pdf_file":pdf_file}
    r_job.format(vars)
    r_job.write(Rscript)
    r_job.run()
    os.system('convert %s %s'%(pdf_file,png_file))
