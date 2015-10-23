#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
Created on Oct 20, 2015

@author: root
'''
import ConfigParser
import os
import sys
import time
from settings import *
from jinja2 import Environment,FileSystemLoader
import operator



def get_html(cfg_in,vars=None):
    command = []
    var_html = {}
    
    reload(sys)
    sys.setdefaultencoding('utf-8')
    work = Work(DEFAULT_CONFIG_DIR + '/get_html_2.cfg')
    work.set_params(cfg_in,vars)
    work.load_default_config()
    config = work.config
    
    
    work_dir = config.get('params','work_dir')
    group_files = config.get('params','group_files')
    job_id = config.get('params','job_id')
    data_type = config.get('params','data_type')
    html_template = config.get('params','html_template')
    
    outfiles = config.get_section('outfiles')
    scripts = config.get_section('scripts')
    
    out_dir_report=work_dir+'/'+'report/'
    os.makedirs(out_dir_report)
    image_dir = out_dir_report+'/images/'
    origin = config.items('origin')
    
    group_files = re.split('\s+',config.get('params','group_files'))
    group_file_origin =group_files[0]
    group_file = re.search('.+\/(.+)\..+', group_file_origin).group(1) 
    #     copy html-demo
    command.append('cp -rf '+html_template+'/* '+out_dir_report+'\n')
    for key,value in origin:
        if(config.has_option('origin', key)):
            match = re.match(r".*png$",value)
            if(match):
                    value_rep = value.replace("#group",group_file)
                    command.append('cp '+work_dir+'../'+value_rep+' '+image_dir+'\n')
            else:
                continue
        else:
            print '06_get_html.cfg no have '+key
    command.append('python %s -c %s '%(scripts['get_html'],config.get('outfiles','config')))
    work.commands.append(''.join(command))
    
    
    return outfiles
if __name__ == '__main__':
    config = sys.argv[1]
    get_html(config)
    
