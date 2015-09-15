from __future__ import division
import re
import os
import sys
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/src')
sys.path.insert(1,this_script_path + '/bin')
from Work import Work,SubWork,MyConfigParser

from work_00 import work_00_merge
#from work_01 import work_01_pick_otu

def pipeline(cfg_file):
    work_pipeline = Work()
    cfg_all = work_pipeline.read_config(cfg_file)
    work_00_out = None
    if not cfg_all.get('all','fna_file'):
        work_00_out = work_00_merge(cfg_all)
#        work_01_out = work_01_pick_otu(work_00_out)
    return cfg_all
   
