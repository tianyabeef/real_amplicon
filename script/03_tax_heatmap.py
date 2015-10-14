#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys
import argparse
import os
this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
import RParser as rp


def read_params(args):
    parser = argparse.ArgumentParser(description='''tax heatmap | v1.0 at 2015/10/13 by liangzb ''')
    parser.add_argument('-i', '--otu_profile', dest='otu_table', metavar='FILE', type=str, required=True,
                        help="set the otu_table_L6.txt")
    parser.add_argument('-g', '--group_file', dest='group', metavar='FILE', type=str, required=True,
                        help="set the group file")
    parser.add_argument('-o', '--out_dir', dest='out_dir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    args = parser.parse_args()
    params = vars(args)
    return params

def work(infile,outfile,showed_rows):
    showed_list = []
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
            if n / len(tabs) >= 0.5:
                showed_list.append(tax[3:])
    with open(showed_rows,'w') as fp:
        for line in showed_list:
            fp.write(line + '\n')

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(params['out_dir']):
        os.mkdir(params['out_dir'])
    for_plot = params['out_dir'] + '/for_plot.txt'
    showed_rows = params['out_dir'] + '/showed_rows.txt'
    pdf_file = params['out_dir'] + '/heatmap.pdf'
    png_file = params['out_dir'] + '/heatmap.png'

    work(params['otu_table'], for_plot, showed_rows)

    vars = {'heatmap_profile':for_plot,
            'show_rowname':showed_rows,
            'pdf_file':pdf_file,
            'group':params['group'],
            'top':30}
    r_job = rp.RParser()
    r_job.open(this_script_path + '/../src/template/03_tax_heatmap.Rtp')
    r_job.format(vars)
    r_job.write(params['out_dir'] + '/heatmap.R')
    r_job.run()
    os.system('convert %s %s'%(pdf_file,png_file))

