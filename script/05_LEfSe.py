#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import sys
import os
import argparse
from util import mkdir

this_script_path = os.path.dirname(__file__)
sys.path.insert(1, '/data_center_01/pipeline/16S_ITS_pipeline_v3.0/script/../src')
from Parser import parse_group_file


def read_params(args):
    parser = argparse.ArgumentParser(description='a wrapper for LEfSe | v1.0 at 2015/10/19 by liangzb')
    parser.add_argument('-i', '--summarize_all', dest='infile', metavar='FILE', type=str, required=True,
                        help="set hte otu_table_all.txt produced by 02_summarize_trans.py")
    parser.add_argument('-l', '--LEfSe_path', dest='LEfSe_path', metavar='DIR', type=str, default=None,
                        help="set the LEfSe path, default find in env")
    parser.add_argument('-g', '--group_file', dest='group', metavar='FILE', type=str, required=True,
                        help="set the group file")
    parser.add_argument('-o', '--out_dir', dest='out_dir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    parser.add_argument('--LDA', dest='LDA', metavar='FLOAT', type=float, default=2,
                        help="set the LDA cutoff, [default is 2]")
    parser.add_argument('--class_row', dest='c', metavar='INT', type=int, default=1,
                        help="set the class row, [default is 1]")
    parser.add_argument('--subject_row', dest='u', metavar='INT', type=int, default=2,
                        help="set the subject row, [default is 2]")
    args = parser.parse_args()
    params = vars(args)
    params['group'] = parse_group_file(params['group'])
    if params['LEfSe_path'] is None:
        params['LEfSe_path'] = ''
    else:
        params['LEfSe_path'] += '/'
    return params


def do_format(infile, outfile, group):
    groups = []
    with open(infile) as in_fp, open(outfile, 'w') as out_fp:
        head = in_fp.next()
        samples = head.strip().split('\t')[1:]
        remain_samples = []
        ind_list = []
        for ind, sample in enumerate(samples):
            try:
                groups.append(group[sample])
                remain_samples.append(sample)
                ind_list.append(ind)
            except KeyError, ex:
                print('%s sample in not in the group_file' % ex)
                continue
        samples = remain_samples
        out_fp.write('class\t%s\n' % '\t'.join(groups))
        out_fp.write('Taxon\t%s\n' % '\t'.join(samples))
        for line in in_fp:
            tabs = line.strip().split('\t')
            tmp = []
            for ind_t, sample_t in enumerate(tabs):
                xiabiao = ind_t - 1
                if xiabiao in ind_list:
                    tmp.append(sample_t)
            if tabs[0].endswith('Other'):
                continue
            if tabs[0].endswith('norank'):
                continue
            if tabs[0].endswith('unclassfied'):
                continue
            tabs[0] = tabs[0].replace(';', '|')
            out_fp.write(tabs[0] + '\t')
            out_fp.write('\t'.join(tmp) + '\n')


def get_commands(infile, LEfSe_path, out_dir, LDA, c, u):
    commands = []
    command='source /home/songwf/.bashrc'
    commands.append(command)
    command = '%sformat_input.py %s %s/LDA.in -c %s -u %s -o 1000000' % (LEfSe_path, infile, out_dir, c, u)
    commands.append(command)
    command = '%srun_lefse.py %s/LDA.in %s/LDA.res -l %s' % (LEfSe_path, out_dir, out_dir, LDA)
    commands.append(command)
    command = '%splot_res.py %s/LDA.res %s/LDA.pdf --format pdf --dpi 150 --width 16' % (LEfSe_path, out_dir, out_dir)
    commands.append(command)
    command = '%splot_res.py %s/LDA.res %s/LDA.png --format png --dpi 150 --width 16' % (LEfSe_path, out_dir, out_dir)
    commands.append(command)
    command = '%splot_cladogram.py %s/LDA.res %s/LDA.cladogram.pdf --format pdf --dpi 150' % (
        LEfSe_path, out_dir, out_dir)
    commands.append(command)
    command = '%splot_cladogram.py %s/LDA.res %s/LDA.cladogram.png --format png --dpi 150' % (
        LEfSe_path, out_dir, out_dir)
    commands.append(command)
    command='source deactivate'
    commands.append(command)
    if not os.path.isdir('%s/biomarkers_raw_images' % out_dir):
        os.mkdir('%s/biomarkers_raw_images' % out_dir)
    command = '%(LEfSe_path)splot_features.py %(out_dir)s/LDA.in %(out_dir)s/LDA.res %(out_dir)s/biomarkers_raw_images/ --format pdf --dpi 200' % {
        'LEfSe_path': LEfSe_path, 'out_dir': out_dir}
    commands.append(command)
    return commands


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['out_dir'])
    for_analysis = '%s/otu_table_for_lefse.txt' % params['out_dir']
    do_format(params['infile'], for_analysis, params['group'])
    commands = get_commands(for_analysis, params['LEfSe_path'], params['out_dir'],
                            params['LDA'], params['c'], params['u'])
    with open(params['out_dir'] + '/commands.sh', 'w') as fp:
        fp.write('\n'.join(commands))
    for command in commands:
        os.system(command)
