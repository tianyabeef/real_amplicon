#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from settings import *

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
    return outfiles

if __name__ == '__main__':
    config = sys.argv[1]
    taxanomy_group(config)


