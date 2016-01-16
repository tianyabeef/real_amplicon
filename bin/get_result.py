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
    outfiles = config.get_section('outfiles')
    out_dir_results = outfiles['out_dir']
    outfiles = config.get_section('outfiles') 
    scripts = config.get_section('scripts')

    os.system('rm -Rf %s' % out_dir_results)
    command = ''
    command += 'python %s --config %s' % (scripts['get_result'], outfiles['config'])
    work.commands.append(command) 
    return outfiles


if __name__ == '__main__':
    config = sys.argv[1]
    get_result(config)
