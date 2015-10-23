#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
Created on Oct 19, 2015

@author: root
'''
from settings import *
import os
import sys
import time
import re
import ConfigParser
def get_result(cfg_in,vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/get_html.cfg')
    work.set_params(cfg_in,vars)
    work.load_default_config()
    config = work.config
    outfiles = config.get_section('outfiles')    
    work_dir = config.get('params','work_dir')
    group_files = config.get('params','group_files')
    out_dir_results=work_dir+'/'+'results/'
    os.makedirs(out_dir_results)
    os.mkdir(out_dir_results+"/01_Reads/")
    os.mkdir(out_dir_results+"/02_OTU/")
    os.mkdir(out_dir_results+"/02_OTU/all/")
    os.mkdir(out_dir_results+"/03_Alpha_diversity/")
    os.mkdir(out_dir_results+"/03_Alpha_diversity/total_alpha_rare")
    os.mkdir(out_dir_results+"/04_Beta_diversity/")
    os.mkdir(out_dir_results+"/05_diff_marder/")
#    config = ConfigParser.SafeConfigParser()
#    config.read("./06_get_html.cfg")
    origin = config.items('origin')
    command = ''
    group_files = re.split('\s+',config.get('params','group_files'))
    for group_file in group_files:
        analysis_name = re.search('.+\/(.+)\..+', group_file).group(1)
        os.mkdir(out_dir_results+"/02_OTU/"+analysis_name)
	os.mkdir(out_dir_results+"/03_Alpha_diversity/"+analysis_name)
	os.mkdir(out_dir_results+"/04_Beta_diversity/"+analysis_name)
	os.mkdir(out_dir_results+"/05_diff_marder/"+analysis_name)
    for key,value in origin:
        if(config.has_option('target', key)):
            match = re.match(r".*#group.*",value)
            if(match):
                for group_file in group_files:
		    analysis_name = re.search('.+\/(.+)\..+', group_file).group(1)
                    value_rep = value.replace("#group",analysis_name)
                    command += 'cp '+work_dir+'../'+value_rep+' '+out_dir_results+config.get('target',key).replace("#group",analysis_name)+'\n'
            else:
                command += 'cp '+work_dir+'../'+value+' '+out_dir_results+config.get('target', key)+'\n'
        else:
            print '06_get_html.cfg target section no have '+key
    work.commands.append(command)
    return outfiles
if __name__ == '__main__':
    config = sys.argv[1]
    get_result(config)
