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


def makedir(dir):
    if os.path.isdir(dir):
        return None
    if dir == '':
        return None
    os.system('mkdir -p %s' % dir)


def makedirs(dirs):
    for dir in dirs:
        makedir(dir)


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

    origin = config.items('origin')
    command = ''
    group_files = re.split('\s+', config.get('params', 'group_files'))

    regex = re.compile('.+\/(.+)\..+')

    for key, value in origin:
        if config.has_option('target', key):
            match = re.match(r".*#group.*", value)
            if match:
                for group_file in group_files:
                    analysis_name = re.search(regex, group_file).group(1)
                    value_rep = value.replace("#group", analysis_name)
                    target_file = out_dir_results + config.get('target', key).replace("#group", analysis_name)
                    makedir(os.path.dirname(target_file))
                    match = re.match(r".*dir$",key)
                    if match:
                        command += 'cp -rf ' + work_dir + '../' + value_rep + '/*.png '
                        command += target_file + '\n'
                        command += 'cp -rf ' + work_dir + '../' + value_rep + '/*.pdf '
                        command += target_file + '\n'
                        command += 'cp -rf ' + work_dir + '../' + value_rep + '/*.txt '
                        command += target_file + '\n'
                    else:
                        command += 'cp -rf ' + work_dir + '../' + value_rep + ' '
                        command += target_file + '\n'
            else:
                target_file = out_dir_results + config.get('target', key)
                makedir(os.path.dirname(target_file))
                match = re.match(r".*dir$",key)
                if match:
                    command += 'cp -rf ' + work_dir + '../' + value + '/*.txt ' + target_file + '\n'
                    command += 'cp -rf ' + work_dir + '../' + value + '/*.pdf ' + target_file + '\n'
                    command += 'cp -rf ' + work_dir + '../' + value + '/*.png ' + target_file + '\n'
                else:
                    command += 'cp -rf ' + work_dir + '../' + value + ' ' + target_file + '\n'
        else:
            sys.stderr.write('06_get_html.cfg target section no have ' + key + '\n')
    work.commands.append(command)
    for docs in os.listdir(params['docs_dir']):
        if docs.find(params['data_type']) >= 0:
            origin = '%s/%s' % (params['docs_dir'], docs)
            target_file = '%s/%s' % (outfiles['out_dir'], docs)
            makedir(os.path.dirname(target_file))
            work.commands.append('cp -rf %s %s' % (origin, target_file))
    return outfiles


if __name__ == '__main__':
    config = sys.argv[1]
    get_result(config)
