#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from settings import *


def beta_ANOSIM_ADONIS(cfg_in, vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/beta_ANOSIM_ADONIS.cfg')
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
    # make mapfile
    group_files = params['group_files'].strip()
    work.commands.append('%s -g %s -o %s'%(scripts['make_mapfile'],
                                           group_files,
                                           outfiles['mapfile']))
    # compare_categories
    work.commands.append('%s --compare_categories %s -d %s -m %s -o %s'%(scripts['run_ANOSIM_ADONIS'],
                                                                         qiime['compare_categories'],
                                                                         outfiles['beta_div_dir'],
                                                                         outfiles['mapfile'],
                                                                         outfiles['ANOSIM_ADONIS_dir']))
    return outfiles


if __name__ == '__main__':
    config = sys.argv[1]
    beta_ANOSIM_ADONIS(config)
