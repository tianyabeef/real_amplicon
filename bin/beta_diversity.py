#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from settings import *


def beta_diversity(cfg_in, vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/beta_diversity.cfg')
    work.set_params(cfg_in, vars)
    work.load_default_config()

    config = work.config
    params = config.get_section('params')
    outfiles = config.get_section('outfiles')
    qiime = config.get_section('qiime')
    scripts = config.get_section('scripts')
    sample_num_in_groups, \
    min_sample_num_in_groups, \
    sample_num_total, \
    group_num = parse_group(params['group'])

    # beta div
    work.commands.append('%s -i %s -o %s -t %s' % (qiime['beta_diversity'],
                                                   params['otu_biom'],
                                                   outfiles['beta_div_dir'],
                                                   params['tree_file']))
    # beta heatmap
    if sample_num_total >= 4:
        work.commands.append('%s -d %s -g %s -o %s' % (scripts['beta_heatmap'],
                                                       outfiles['beta_div_dir'],
                                                       params['group'],
                                                       outfiles['beta_heatmap_dir']))
    # beta pcoa
    if min_sample_num_in_groups >= 5 and group_num >= 2:
        with_boxplot = '--with_boxplot'
    else:
        with_boxplot = '--without_boxplot'
    if sample_num_total >= 5:
        work.commands.append('%s -d %s -g %s -o %s %s' % (scripts['beta_pcoa'],
                                                          outfiles['beta_div_dir'],
                                                          params['group'],
                                                          outfiles['beta_pcoa_dir'],
                                                          with_boxplot))
    # beta nmds
    if min_sample_num_in_groups >= 5 and group_num >= 2:
        with_boxplot = '--with_boxplot'
    else:
        with_boxplot = '--without_boxplot'
    if sample_num_total >= 5:
        work.commands.append('%s -d %s -g %s -o %s %s' % (scripts['beta_nmds'],
                                                          outfiles['beta_div_dir'],
                                                          params['group'],
                                                          outfiles['beta_nmds_dir'],
                                                          with_boxplot))
    # beta anosim
    if min_sample_num_in_groups >= 5 and group_num >= 2:
        work.commands.append('%s -d %s -g %s -o %s' % (scripts['beta_anosim'],
                                                       outfiles['beta_div_dir'],
                                                       params['group'],
                                                       outfiles['beta_anosim_dir']))

    # beta mrpp
    if min_sample_num_in_groups >= 5 and group_num >= 2:
        work.commands.append('%s -d %s -g %s -o %s' % (scripts['beta_mrpp'],
                                                       outfiles['beta_div_dir'],
                                                       params['group'],
                                                       outfiles['beta_mrpp_dir']))

    # beta cluster
    if sample_num_total >= 5:
        command = '%s --jackknifed_beta_diversity %s --make_bootstrapped_tree %s ' % (scripts['beta_cluster'],
                                                                                      qiime['jackknifed_beta_diversity'],
                                                                                      qiime['make_bootstrapped_tree'])
        command += '-i %s -o %s -t %s ' % (params['otu_biom'],
                                           outfiles['beta_cluster_dir'],
                                           params['tree_file'])
        if params['seqs_per_sample']:
            command += '-s %s' % params['seqs_per_sample']
        else:
            command += '--stat_file %s --group_file %s' % (params['stat_file'], params['group'])
        work.commands.append(command)

    return outfiles


if __name__ == '__main__':
    config = sys.argv[1]
    beta_diversity(config)
