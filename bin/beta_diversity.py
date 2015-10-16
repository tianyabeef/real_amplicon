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

    # beta div
    work.commands.append('%s -i %s -o %s -t %s'%(qiime['beta_diversity'],
                                                 params['otu_biom'],
                                                 outfiles['beta_div_dir'],
                                                 params['tree_file']))
    # beta heatmap
    work.commands.append('%s -d %s -g %s -o %s'%(scripts['beta_heatmap'],
                                                 outfiles['beta_div_dir'],
                                                 params['group'],
                                                 outfiles['beta_heatmap_dir']))
    # beta cluster
    command = '%s --jackknifed_beta_diversity %s --make_bootstrapped_tree %s '%(scripts['beta_cluster'],
                                                                                qiime['jackknifed_beta_diversity'],
                                                                                qiime['make_bootstrapped_tree'])
    command += '-i %s -o %s -t %s '%(params['otu_biom'],
                                     outfiles['beta_cluster_dir'],
                                     params['tree_file'])
    if params['seqs_per_sample']:
        command += '-s %s'%params['seqs_per_sample']
    else:
        command += '--stat_file %s --group_file %s'%(params['stat_file'],params['group'])
    work.commands.append(command)

    return outfiles


if __name__ == '__main__':
    config = sys.argv[1]
    beta_diversity(config)
