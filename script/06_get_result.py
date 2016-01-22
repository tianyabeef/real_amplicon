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
import ConfigParser

this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../bin')
from Work import Work


def get_section(config, section):
    var = {}
    for item in config.items(section):
        var[item[0]] = item[1]
    return var


def read_params(args):
    parser = argparse.ArgumentParser(description=''' ''')
    parser.add_argument('--config', dest='config', metavar='FILE', type=str, required=True,
                        help="set the config file")
    args = parser.parse_args()
    params = vars(args)
    return params


def check_filename(file_name):
    if not file_name:
        return False
    filter_suffix = ['R', 'log', 'Rout', 'pl', 'py', 'pyc', 'sh', 'alpha_div', 'rarefaction', 'cfg']
    for suf in filter_suffix:
        if file_name.endswith(suf):
            return False
    return True


def get_result(config_file):
    config = ConfigParser.ConfigParser()
    config.read(config_file)

    # work = Work(config_file)
    # work.load_default_config()
    # config = work.config
    work_dir = config.get('params', 'work_dir')
    group_names = re.split('\s+', config.get('params', 'group_files'))
    out_dir_results = config.get('outfiles', 'out_dir')
    origin = get_section(config, 'origin')
    target = get_section(config, 'target')

    for key, value in origin.iteritems():
        origin[key] = '%s/../%s' % (work_dir, value)

    for key, value in target.iteritems():
        target[key] = '%s/%s' % (out_dir_results, value)

    regex = re.compile('.+\/(.+)\..+')
    group_reg = re.compile(r".*#group.*")

    for key, value in origin.iteritems():
        if key in target:
            match = group_reg.match(value)
            if match:
                for group_name in group_names:
                    analysis_name = regex.search(group_name).group(1)
                    value_rep = value.replace("#group", analysis_name)
                    target_file = target[key].replace("#group", analysis_name)
                    mkdir(os.path.dirname(target_file))
                    if re.match(r".*dir$", key):
                        try:
                            for file_name in os.listdir(value_rep):
                                file_name = '%s/%s' % (value_rep, file_name)
                                if check_filename(file_name):
                                    os.system('cp -rf %s %s' % (file_name, target_file))
                        except OSError:
                            sys.stderr.write('%s dir not found!\n' % value_rep)
                    else:
                        if check_filename(value_rep):
                            os.system('cp -rf %s %s' % (value_rep, target_file))
            else:
                target_file = target[key]
                mkdir(os.path.dirname(target_file))
                match = re.match(r".*dir$", key)
                if match:
                    try:
                        for file_name in os.listdir(value):
                            file_name = '%s/%s' % (value, file_name)
                            if check_filename(file_name):
                                os.system('cp -rf %s %s' % (file_name, target_file))
                    except OSError:
                        sys.stderr.write('%s dir not found!\n' % value)
                else:
                    if check_filename(value):
                        os.system("cp -rf %s %s" % (value, target_file))
        else:
            sys.stderr.write('06_get_html.cfg target section no have ' + key + '\n')

    for docs in os.listdir(config.get('params', 'docs_dir')):
        if docs.find(config.get('params', 'data_type')) >= 0:
            origin = '%s/%s' % (config.get('params', 'docs_dir'), docs)
            target_file = '%s/%s' % (out_dir_results, docs)
            mkdir(os.path.dirname(target_file))
            os.system('cp -rf %s %s' % (origin, target_file))


if __name__ == '__main__':
    params = read_params(sys.argv)
    get_result(params['config'])
