#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys
import argparse
import os
from util import mkdir
this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
import Parser as rp


def read_params(args):
    parser = argparse.ArgumentParser(description='''tax heatmap | v1.0 at 2015/10/13 by liangzb ''')
    parser.add_argument('-i', '--otu_profile', dest='otu_table', metavar='FILE', type=str, required=None,
                        help="set the otu_table_L6.txt")
    parser.add_argument('-f', '--for_plot', dest='for_plot', metavar='FILE', type=str, default=None,
                        help="set the profile for plot, if set this param, otu_table will not work, \
                              one of otu_profile and for_plot is required")
    parser.add_argument('-g', '--group_file', dest='group', metavar='FILE', type=str, required=True,
                        help="set the group file")
    parser.add_argument('-o', '--out_dir', dest='out_dir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    parser.add_argument('-t', '--top', dest='top', metavar='INT', type=str, default='30',
                        help="set the top num, [default is 30]")
    args = parser.parse_args()
    params = vars(args)
    if params['top'] != 'all':
        params['top'] = int(params['top'])
    if params['for_plot'] is None and params['otu_table'] is None:
        parser.print_help()
        sys.exit()
    if params['for_plot'] is None:
        params['for_plot'] = params['out_dir'] + '/for_plot.txt'
        work(params['otu_table'],params['for_plot'])
    return params

def work(infile,outfile):
#    showed_list = []
    with open(infile) as in_fp, open(outfile,'w') as out:
        head = in_fp.next()
        if head.startswith('# Constructed from biom'):
            head = in_fp.next()
        out.write(head.strip('#'))
        for line in in_fp:
            tabs = line.strip().split('\t')
            taxes = tabs[0].split(';')
            for tax in taxes:
                if tax.startswith('g__'):
                    tabs[0] = tax[3:]
                    break
            else:
                continue
            out.write('\t'.join(tabs) + '\n')
            n = 0
            for tab in tabs[1:]:
                if float(tab) > 0:
                    n += 1
#            if n / len(tabs) >= 0.5:
#                showed_list.append(tax[3:])
#    with open(showed_rows,'w') as fp:
#        for line in showed_list:
#            fp.write(line + '\n')

if __name__ == '__main__':
    params = read_params(sys.argv)
    print params['for_plot']
    mkdir(params['out_dir'])
#    showed_rows = params['out_dir'] + '/showed_rows.txt'
    pdf_file = params['out_dir'] + '/heatmap.pdf'
    png_file = params['out_dir'] + '/heatmap.png'

#    work(params['otu_table'], pfor_plot)

    vars = {'heatmap_profile':params['for_plot'],
#            'show_rowname':showed_rows,
            'pdf_file':pdf_file,
            'group':params['group'],
            'top':params['top']}
    r_job = rp.Rparser()
    r_job.open(this_script_path + '/../src/template/03_tax_heatmap.Rtp')
    r_job.format(vars)
    r_job.write(params['out_dir'] + '/heatmap.R')
    r_job.run()
    os.system('convert %s %s'%(pdf_file,png_file))
