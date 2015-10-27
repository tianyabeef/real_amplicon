#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from settings import *

def commands_factory(infile,outdir,mode,vars):
    scripts = vars['scripts']
    params = vars['params']
    commands = []
    commands.append('%s -i %s -o %s -m %s'%(scripts['trans_profile'],
                                             infile,
                                             outdir + '/profile.for_analysis.txt',
                                             mode))
    commands.append('%s -i %s -o %s -g %s -c %s'%(scripts['tax_diff'],
                                                  outdir + '/profile.for_analysis.txt',
                                                  outdir,
                                                  params['group'],
                                                  params['p_cutoff']))
    # pca
    if vars['sample_num_total'] >= 5:
        marker_profile = outdir + '/profile.for_plot_p_%s.txt'%params['p_cutoff']
        commands.append('%s -i %s -o %s -g %s'%(scripts['diff_pca'],
                                                marker_profile,
                                                outdir,
                                                params['group']))
    # heatmap
    if vars['sample_num_total'] >=4:
        commands.append('%s -f %s -o %s -g %s -t %s'%(scripts['diff_heatmap'],
                                                    marker_profile,
                                                    outdir,
                                                    params['group'],
                                                    params['heatmap_top']))
    # boxplot
    if vars['min_sample_num_in_groups'] >= 5:
        commands.append('%s -i %s -o %s -g %s -t %s'%(scripts['diff_boxplot'],
                                                    marker_profile,
                                                    outdir,
                                                    params['group'],
                                                    params['boxplot_top']))
    os.system('mkdir -p %s'%outdir)
    with open(outdir + '/commands.sh','w') as cmd:
        cmd.write('\n'.join(commands))

    return commands

def taxanomy_diff(cfg_in,vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/taxanomy_diff.cfg')
    work.set_params(cfg_in,vars)
    work.load_default_config()

    config = work.config
    params = config.get_section('params')
    scripts = config.get_section('scripts')
    outfiles = config.get_section('outfiles')
    softwares = config.get_section('softwares')
    sample_num_in_groups,\
    min_sample_num_in_groups,\
    sample_num_total,\
    group_num = parse_group(params['group'])

    #  LEfSe analysis
    work.commands.append('%s -i %s -l %s -g %s -o %s'%(scripts['LEfSe'],
                                                       params['summarize_dir'] + '/otu_table_all.txt',
                                                       softwares['LEfSe_dir'],
                                                       params['group'],
                                                       outfiles['LEfSe_outdir']))
    vars = {
        'min_sample_num_in_groups' : min_sample_num_in_groups,
        'sample_num_total' : sample_num_total,
        'scripts' : scripts,
        'params' : params,
    }
    # otu level
    work.commands += commands_factory(params['uniform_profile'],outfiles['otu_diff_outdir'],'otu',vars)

    # all level
    work.commands += commands_factory(params['summarize_dir'] + '/otu_table_all.txt',outfiles['taxall_diff_outdir'],'all',vars)

    # phylum level
    work.commands += commands_factory(params['summarize_dir'] + '/otu_table_L2.txt',outfiles['phylum_diff_outdir'],'phylum',vars)

    # genus level
    work.commands += commands_factory(params['summarize_dir'] + '/otu_table_L6.txt',outfiles['genus_diff_outdir'],'genus',vars)


    return outfiles

if __name__ == '__main__':
    config = sys.argv[1]
    taxanomy_diff(config)

