#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import sys
import argparse
import os
from util import mkdir, image_trans
from collections import defaultdict

this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
import Parser as rp
from Parser import parse_group_file
import pandas as pd

def read_params(args):
    parser = argparse.ArgumentParser(description='''diff boxplot | v1.0 at 2015/10/26 by liangzb ''')
    parser.add_argument('-i', '--infile', dest='infile', metavar='file', type=str, required=True,
                        help="set the marker profile file in")
    parser.add_argument('-o', '--outdir', dest='outdir', metavar='DIR', type=str, required=True,
                        help="set the work dir")
    parser.add_argument('-g', '--group', dest='group', metavar='FILE', type=str, required=True,
                        help="set the group file")
    parser.add_argument('-t', '--top', dest='top', metavar='INT', type=str, default='20',
                        help="set the top num, [default is 20], show all by set it 'all'")
    args = parser.parse_args()
    params = vars(args)
    if params['top'] != 'all':
        params['top'] = int(params['top'])
    else:
        params['top'] = None
    params['group'] = parse_group_file(params['group'])
    params['for_plot'] = params['outdir'] + '/diff_boxplot.for_plot_top_%s.txt' % params['top']
    return params


class Sample(object):
    def __init__(self, name):
        self.name = name
        self.profiles = defaultdict(float)


class Group(object):
    def __init__(self, name):
        self.name = name
        self.samples = {}


def get_table(params):
    sample_dict = {}
    group_dict = {}
    profile_total = defaultdict(float)
    data = pd.DataFrame.from_csv(params['infile'],sep="\t")
    data.index.name="Name"
    data.to_csv(params['infile'],sep="\t")
    with open(params['infile']) as fp:
        samples = fp.next().strip().split('\t')[1:]
        for sample in samples:
            group = params['group'][sample]
            if group not in group_dict:
                group_dict[group] = Group(group)
            s = Sample(sample)
            sample_dict[sample] = s
            group_dict[group].samples[sample] = s
        for line in fp:
            tabs = line.strip().split('\t')
            tax_name = tabs.pop(0)
            for ind, tab in enumerate(tabs):
                sample_dict[samples[ind]].profiles[tax_name] += float(tab)
                profile_total[tax_name] += float(tab)
    return profile_total, group_dict


def check_zero(group_dict, tax):
    out_str = ''
    for group in group_dict.itervalues():
        group_total = 0
        for sample in group.samples.itervalues():
            group_total += sample.profiles[tax]
            out_str += '%s\t%s\t%s\t%s\n' % (sample.name, tax, sample.profiles[tax], group.name)
        if group_total == 0:
            return None
    return out_str


def write(profile_total, group_dict, outfile, top):
    tax_all = list(profile_total.iterkeys())
    n = 0
    with open(outfile, 'w') as out:
        out.write('Sample\tTax\tProfile\tGroup\n')
        for tax in sorted(tax_all, cmp=lambda a, b: cmp(profile_total[b], profile_total[a])):
            if top and n >= top:
                break
            out_str = check_zero(group_dict, tax)
            if out_str is not None:
                out.write(out_str)
                n += 1


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['outdir'])
    profile_total, group_dict = get_table(params)
    write(profile_total, group_dict, params['for_plot'], params['top'])

    r_job = rp.Rparser()
    r_job.open(this_script_path + '/../src/template/05_diff_boxplot.Rtp')
    r_file = params['outdir'] + '/diff_boxplot.R'
    pdf_file = params['outdir'] + '/diff_boxplot.pdf'
    png_file = params['outdir'] + '/diff_boxplot.png'
    var = {
        'for_plot': params['for_plot'],
        'pdf_file': pdf_file
    }
    r_job.format(var)
    r_job.write(r_file)
    r_job.run()
    image_trans(pdf_file, png_file)
