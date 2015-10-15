#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from settings import *


def alpha_diversity(cfg_in, vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/alpha_diversity.cfg')
    work.set_params(cfg_in, vars)
    work.load_default_config()

    config = work.config
    params = config.get_section('params')
    outfiles = config.get_section('outfiles')
    qiime = config.get_section('qiime')
    scripts = config.get_section('scripts')

    # alpha_boxplot
    work.commands.append('%s -a %s -m %s -o %s'%(scripts['alpha_boxplot'],
                                                 params['alpha_div_collate_dir'],
                                                 params['alpha_metrics'],
                                                 outfiles['alpha_boxplot_dir']))

    return outfiles


if __name__ == '__main__':
    config = sys.argv[1]
    alpha_diversity(config)
