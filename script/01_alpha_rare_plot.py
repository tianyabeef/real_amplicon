#!/usr/bin/env python
from __future__ import division
import sys
import os
import argparse
from util import mkdir
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/../src')
import Parser as rp

def read_params(args):
    parser = argparse.ArgumentParser(description='plot alpha rare | v1.0 at 2015/09/28 by liangzb')
    parser.add_argument('-g','--groupfile',dest='group_file',metavar='FILE',type=str,required=True,
            help="set the group file")
    parser.add_argument('-d','--indir',dest='indir',metavar='INDIR',type=str,required=True,
            help="set the directory of the alpha collate")
    parser.add_argument('-o','--outdir',dest='outdir',metavar='OUTDIR',type=str,required=True,
            help="set the output directory")
    parser.add_argument('-a','--alpha_metrics',dest='alpha_metrics',metavar='STR',type=str,required=True,
            help="set the alpha names")

    args = parser.parse_args()
    params = vars(args)
    params['alphas'] = params['alpha_metrics'].split(',')
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['outdir'])
    r_job = rp.Rparser()
    r_job.open(this_script_path + '/../src/template/01_alpha_rare.Rtp')
    for alpha in params['alphas']:
        otu_table = '%s/%s.txt'%(params['indir'],alpha)
        pdf_file = '%s/%s.pdf'%(params['outdir'],alpha)
        png_file = '%s/%s.png'%(params['outdir'],alpha)
        vars = {"otu_table":otu_table,
                "group_file":params['group_file'],
                "pdf_file":pdf_file,
                'alpha_name':alpha}
        r_job.format(vars)
        r_job.write('%s/%s.R'%(params['outdir'],alpha))
        r_job.run()
        os.system('convert %s %s'%(pdf_file,png_file))
