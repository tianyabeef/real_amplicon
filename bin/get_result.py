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

def makedirs(dirs):
    for dir in dirs:
        if os.path.isdir(dir):
            return None
        if dir == '':
            return None
        os.system('mkdir -p %s'%dir)

def get_result(cfg_in,vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/get_result.cfg')
    work.set_params(cfg_in,vars)
    work.load_default_config()
    config = work.config
    params = config.get_section('params')
    outfiles = config.get_section('outfiles')
    work_dir = params['work_dir']
    group_files = params['group_files']
    out_dir_results = outfiles['out_dir']

    os.system('rm -Rf %s'%out_dir_results)
    dirs = []
    dirs.append(out_dir_results+"/01_Reads/")
    dirs.append(out_dir_results+"/02_OTU/all/wf_taxa_summary/")
    dirs.append(out_dir_results+"/02_OTU/all/bar_plot/phylum/")
    dirs.append(out_dir_results+"/02_OTU/all/bar_plot/order/")
    dirs.append(out_dir_results+"/02_OTU/all/bar_plot/class/")
    dirs.append(out_dir_results+"/02_OTU/all/bar_plot/genus/")
    dirs.append(out_dir_results+"/02_OTU/all/bar_plot/family/")
    dirs.append(out_dir_results+"/03_Alpha_diversity/total_alpha_rare/")
    dirs.append(out_dir_results+"/04_Beta_diversity/")
    dirs.append(out_dir_results+"/05_diff_analysis/")
    makedirs(dirs)
    origin = config.items('origin')
    command = ''
    group_files = re.split('\s+',config.get('params','group_files'))

    regex = re.compile('.+\/(.+)\..+')

    for group_file in group_files:
        analysis_name = re.search(regex, group_file).group(1)
        dirs = []
        dirs.append(out_dir_results+"/02_OTU/"+analysis_name+"/wf_taxa_summary/")
        dirs.append(out_dir_results+"/02_OTU/"+analysis_name+"/bar_plot/phylum/")
        dirs.append(out_dir_results+"/02_OTU/"+analysis_name+"/bar_plot/order/")
        dirs.append(out_dir_results+"/02_OTU/"+analysis_name+"/bar_plot/class/")
        dirs.append(out_dir_results+"/02_OTU/"+analysis_name+"/bar_plot/genus/")
        dirs.append(out_dir_results+"/02_OTU/"+analysis_name+"/bar_plot/family/")
        dirs.append(out_dir_results+"/03_Alpha_diversity/"+analysis_name)
        dirs.append(out_dir_results+"/04_Beta_diversity/"+analysis_name)
        dirs.append(out_dir_results+"/03_Alpha_diversity/"+analysis_name+"/box_plot/")
        dirs.append(out_dir_results+"/05_diff_analysis/"+analysis_name+"/LEfSe/")
        dirs.append(out_dir_results+"/05_diff_analysis/"+analysis_name+"/otu_diff/")
        dirs.append(out_dir_results+"/05_diff_analysis/"+analysis_name+"/genus_diff/")
        dirs.append(out_dir_results+"/05_diff_analysis/"+analysis_name+"/taxall_diff/")
        dirs.append(out_dir_results+"/05_diff_analysis/"+analysis_name+"/phylum_diff/")
        makedirs(dirs)
    for key,value in origin:
        if(config.has_option('target', key)):
            match = re.match(r".*#group.*",value)
            if(match):
                for group_file in group_files:
                    analysis_name = re.search(regex, group_file).group(1)
                    value_rep = value.replace("#group",analysis_name)
                    command += 'cp -rf '+work_dir+'../'+value_rep+' '+out_dir_results+config.get('target',key).replace("#group",analysis_name)+'\n'
            else:
                command += 'cp -rf '+work_dir+'../'+value+' '+out_dir_results+config.get('target', key)+'\n'
        else:
            sys.stderr.write('06_get_html.cfg target section no have '+key+'\n' )
    work.commands.append(command)
    for docs in os.listdir(params['docs_dir']):
        if docs.find(params['data_type']) >= 0:
            origin = '%s/%s'%(params['docs_dir'],docs)
            target = '%s/%s'%(outfiles['out_dir'],docs)
            work.commands.append('cp -rf %s %s'%(origin,target))
    return outfiles

if __name__ == '__main__':
    config = sys.argv[1]
    get_result(config)
