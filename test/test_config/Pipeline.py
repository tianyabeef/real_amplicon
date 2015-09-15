from __future__ import division
import re

import sys
sys.path.insert(1,'../../src')
from Work import Work

class SubWork(Work):
    def __init__(self,work_id,cfg_in):
        super(SubWork,self).__init__()
        self.work_id = work_id
        self.config.set_section('all',cfg_in.items('all'))
        self.set_script(cfg_in)
        cfg_in.set(work_id,'work_dir',self.config.get('all','work_dir'))
        self.config.set_section(work_id,cfg_in.items(work_id))

    def set_script(self,cfg_in):
        for name,value in cfg_in.items('scripts'):
            if re.search('^%s'%self.work_id,name):
                self.config.set('scripts',name,value)

def pipeline(cfg_file):
    work_pipeline = Work()
    cfg_all = work_pipeline.read_config(cfg_file)
    work_00_merge(cfg_all)

    return cfg_all

def work_00_merge(cfg_in):
    work = SubWork('00',cfg_in)

    out_dir = work.config.get('00','out_dir')
    work.config.add('out_files','merged_file',out_dir + '/16S_together.fna')
    work.config.add('out_files','merged_file',out_dir + '/16S_together.stat')
    work.config.add('out_files','work_shell',out_dir + '/work.sh')
    work.config.add('out_files','cfg_file',out_dir + '/work.cfg')

    script = work.config.get('scripts','00_merge')
    infile_list = work.config.get('00','fq_for_merge')
    out_dir = work.config.get('00','out_dir')
    require = work.config.get('00','require')
    name_table = work.config.get('00','name_table')
    work.commands.append('%s %s %s -r %s -n %s\n'%(script,infile_list,out_dir,require,name_table))

    work.config.remove_option('00','work_dir')
    work.write_config(work.config.get('out_files','cfg_file'))
    work.write_shell(work.config.get('out_files','work_shell'))

    return work.config.get('out_files','work_shell')
    
if __name__ == '__main__':
    pipeline('work.cfg')
