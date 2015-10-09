#!/usr/bin/env python
from __future__ import division
import sys
import os
import re
import argparse
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/../src')
import RParser as rp
from ForBarPlot import Subject

def read_params(args):
    parser = argparse.ArgumentParser(description='tax bar plot | v1.0 at 2015/10/09 by liangzb')
    parser.add_argument('-t','--wf_tax_dir',dest='wf_tax_dir',metavar='DIR',type=str,required=True,
            help="set the wf_taxa_summary dir produced by summarize_taxa.py")
    parser.add_argument('-o','--out_dir',dest='out_dir',metavar='DIR',type=str,required=True,
            help="set the output dir")
    parser.add_argument('-l','--level',dest='level_list',metavar='INTs',nargs='+',type=int,default=[2,6],
            help="set the tax level, 1..7 stands for kingdom..species, [default is 2 6]")

    args = parser.parse_args()
    params = vars(args)
    return params


TAX_LEVEL = ['root','kingdom','phylum','class','order','family','genus','species']

def work(level,params):
    work_dir = '%s/%s'%(params['out_dir'],TAX_LEVEL[level])
    if not os.path.isdir(work_dir):
        os.mkdir(work_dir)
    profile = '%s/otu_table_L%d.txt'%(params['wf_tax_dir'],level)
    outfile = '%s/for_plot.txt'%work_dir
    subject = Subject(profile,outfile)
    subject.run()

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(params['out_dir']):
        os.mkdir(params['out_dir'])
    
    outfile_list = []
    for level in params['level_list']:
        outfile_list.append(work(level,params))

    r_job = rp.RParser()
    r_job.open(this_script_path + '/../src/template/02_bar_plot.Rtp')
    for level in params['level_list']:
        work_dir = '%s/%s'%(params['out_dir'],TAX_LEVEL[level])
        infile = '%s/for_plot.txt'%work_dir
        Rscript = '%s/bar_plot.R'%work_dir
        pdf_file = '%s/bar_plot.pdf'%work_dir
        png_file = '%s/bar_plot.png'%work_dir
        vars = {"infile":infile,
                "pdf_file":pdf_file,
                "title":'%s Level Barplot'%TAX_LEVEL[level].capitalize()}
        r_job.format(vars)
        r_job.write(Rscript)
        r_job.run()
        os.system('convert %s %s'%(pdf_file,png_file))


   
