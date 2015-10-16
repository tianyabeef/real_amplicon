#!/usr/bin/env python
import sys
import argparse
import os
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/../src')
import Parser as rp
from CoreOTU import Subject

def read_params(args):
    parser = argparse.ArgumentParser(description='''core otu analysis | v1.0 at 2015/10/12 by liangzb ''')
    parser.add_argument('-i','--otu_profile',dest='otu_table',metavar='FILE',type=str,required=True,
            help="set the otu table file")
    parser.add_argument('-t','--tax_assignment',dest='tax_ass',metavar='FILE',type=str,required=True,
            help="set the tax assignment file")
    parser.add_argument('-c','--percent_cutoff',dest='cutoff',metavar='FLOAT',type=float,default=1,
            help="set the percent cutoff in [0.8, 0.9, 1], [default is 1]")
    parser.add_argument('-o','--out_dir',dest='out_dir',metavar='DIR',type=str,required=True,
            help="set the output dir")
    args = parser.parse_args()
    params = vars(args)
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(params['out_dir']):
        os.mkdir(params['out_dir'])
    for_plot = params['out_dir'] + '/for_plot.txt'
    core_otu = params['out_dir'] + '/core_otu.txt'
    pdf_file = params['out_dir'] + '/core_otu.pdf'
    png_file = params['out_dir'] + '/core_otu.png'

    subject = Subject(params['otu_table'],params['tax_ass'],
                      for_plot,core_otu,params['cutoff'])
    subject.work()

    r_job = rp.Parser()
    r_job.open(this_script_path + '/../src/template/03_core_otu.Rtp')
    vars = {'for_plot':for_plot,
            'pdf_file':pdf_file}
    r_job.format(vars)
    r_job.write(params['out_dir'] + '/core_otu.R')
    r_job.run()
    os.system('convert %s %s'%(pdf_file,png_file))

