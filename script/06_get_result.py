#!/usr/bin/env python
# -*- coding: utf-8 -*- \#
"""
@author = 'liangzb'
@date = '2016-01-15'

"""

import re
import os
import sys
import argparse
from util import mkdir

this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../bin')
from Work import Work


def read_params(args):
    parser = argparse.ArgumentParser(description=''' ''')
    parser.add_argument('--config', dest='config', metavar='FILE', type=str, required=True,
                        help="set the config file")
    args = parser.parse_args()
    params = vars(args)
    return params


def check_filename(file_name):
    if file_name.endswith('R'):
        return False
    if file_name.startswith('log'):
        return False
    if file_name.endswith('Rout'):
        return False
    return True


def read_config(config_file):
    work = Work(config_file)
    work.load_default_config()
    config = work.config
    params = config.get_section('params')
    outfiles = config.get_section('outfiles')
    work_dir = params['work_dir']
    group_files = params['group_files']
    out_dir_results = outfiles['out_dir']

    origin = config.get_section('origin')
    target = config.get_section('target')

    for key, value in origin.iteritems():
        origin[key] = '%s/%s' % (work_dir, value)

    for key, value in target.iteritems():
        target[key] = '%s/%s' % (out_dir_results, value)


def get_result(outdir, origin, target, params, group_names):
    outdir = params['outdir']
    origin = params['origin']
    target = params['target']
    group_names = params['group_names']
    regex = re.compile('.+\/(.+)\..+')
    group_reg = re.compile(r".*#group.*")

    for key, value in origin:
        if key in target:
            match = group_reg.match(value)
            if match:
                for group_name in group_names:
                    analysis_name = regex.search(group_name).group(1)
                    value_rep = value.replace("#group", analysis_name)
                    target_file = target[key].replace("#group", analysis_name)
                    mkdir(os.path.dirname(target_file))
                    if re.match(r".*dir$", key):
                        for group_name in os.open('ls %s/*' % value_rep).read().rstrip().split('\n'):
                            if check_filename(group_name):
                                os.system('cp -rf %s %s' % (group_name, target_file))
            else:
                target_file = target[key]
                mkdir(os.path.dirname(target_file))
                match = re.match(r".*dir$", key)
                if match:
                    for file_name in os.open('ls %s/*' % value).read().rstrip().split('\n'):
                        if check_filename(file_name):
                            os.system('cp -rf %s %s' % (file_name, target_file))
                else:
                    os.system("cp -rf %s %s" % (value, target_file))
        else:
            sys.stderr.write('06_get_html.cfg target section no have ' + key + '\n')

    for docs in os.listdir(params['docs_dir']):
        if docs.find(params['data_type']) >= 0:
            origin = '%s/%s' % (params['docs_dir'], docs)
            target_file = '%s/%s' % (outdir, docs)
            mkdir(os.path.dirname(target_file))
            os.system('cp -rf %s %s' % (origin, target_file))


if __name__ == '__main__':
    params = read_params(sys.argv)
    read_config(params['config_file'])
    get_result(params)
