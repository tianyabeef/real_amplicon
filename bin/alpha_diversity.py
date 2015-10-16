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
    scripts = config.get_section('scripts')
    sample_num_in_groups,\
    min_sample_num_in_groups,\
    sample_num_total,\
    group_num = parse_group(params['group'])

    # alpha_grouped
    work.commands.append('%s -a %s -g %s -m %s -o %s'%(scripts['alpha_grouped'],
                                                       params['alpha_div_collate_dir'],
                                                       params['group'],
                                                       params['alpha_metrics'],
                                                       outfiles['alpha_grouped']))

    if min_sample_num_in_groups >= 5:
    # alpha_boxplot
        work.commands.append('%s -a %s -m %s -o %s'%(scripts['alpha_boxplot'],
                                                     outfiles['alpha_grouped'],
                                                     params['alpha_metrics'],
                                                     outfiles['alpha_boxplot_dir']))

    if min_sample_num_in_groups >= 3:
    # alpha_diff_test
        work.commands.append('%s -a %s -m %s -o %s'%(scripts['alpha_diff_test'],
                                                     outfiles['alpha_grouped'],
                                                     params['alpha_metrics'],
                                                     outfiles['alpha_diff_dir']))

    return outfiles


if __name__ == '__main__':
    config = sys.argv[1]
    alpha_diversity(config)
