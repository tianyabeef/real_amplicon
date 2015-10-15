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

    return outfiles


if __name__ == '__main__':
    config = sys.argv[1]
    beta_diversity(config)
