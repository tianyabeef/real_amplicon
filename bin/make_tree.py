#!/usr/bin/env python
# -*- coding:utf-8 -*- #
from settings import *

def make_tree(cfg_in, vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/make_tree.cfg')
    work.set_params(cfg_in,vars)
    work.load_default_config()

    config = work.config
    params = config.get_section('params')
    scripts = config.get_section('scripts')
    qiime = config.get_section('qiime')
    outfiles = config.get_section('outfiles')

    command = "%s --align_seq_py %s --make_phylogeny_py %s "%(scripts['make_tree'],
                                                             qiime['align_seqs'],
                                                             qiime['make_phylogeny'])

    if not params['align_method']:
        if params['data_type'] == '16S':
            params['align_method'] = 'pynast'
        elif params['data_type'] == 'ITS':
            params['align_method'] = 'muscle'
    command += '-i %s -a %s -d %s --tree_file %s -o %s '%(params['rep_set'],
                                                          params['align_method'],
                                                          params['data_type'],
                                                          outfiles['tree_file'],
                                                          outfiles['out_dir'])
    if params['align_method'] == 'pynast':
        if not params['pre_align']:
            raise IOError,'must set the pre align file when align_method is pynast'
        command += "-t %s "%params['pre_align']
    if params['lanemask']:
        command += '--filter_alignment_py %s -m %s '%(qiime['filter_alignment'],
                                                      params['lanemask'])
    work.commands.append(command)

    return outfiles

if __name__ == '__main__':
    config = sys.argv[1]
    make_tree(config)
