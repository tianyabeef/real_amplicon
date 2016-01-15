#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on Oct 19, 2015

@author: root
'''
from settings import *
import os
import sys
import re


def get_result(cfg_in, vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/get_result.cfg')
    work.set_params(cfg_in, vars)
    work.load_default_config()
    config = work.config
    params = config.get_section('params')
    outfiles = config.get_section('outfiles')
    work_dir = params['work_dir']
    group_files = params['group_files']
    out_dir_results = outfiles['out_dir']

    os.system('rm -Rf %s' % out_dir_results)



    command = ''
    group_files = re.split('\s+', config.get('params', 'group_files'))

    regex = re.compile('.+\/(.+)\..+')
    return outfiles


if __name__ == '__main__':
    config = sys.argv[1]
    get_result(config)
