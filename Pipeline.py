from __future__ import division
import re
import os
import sys
import argparse
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/bin')
from work_00 import work_00_merge
from work_01 import work_01_pick_otu,work_01_alpha_rare
from work_02 import work_02_otu_table

def read_params(args):
    parser = argparse.ArgumentParser(description='''16S/ITS pipeline v3.0 | at 2015/09/28 by liangzb ''')
    parser.add_argument('-i','--cfg_in',metavar='CFG',dest='cfg',type=str,required=True,
            help="set the cfg file or cfg")
    parser.add_argument('-o','--out_qsub',metavar='STR',dest='qsub',type=str,default='./work.qsub',
            help="set the output qsub shell")

    args = parser.parse_args()
    params = vars(args)
    return params


def pipeline(cfg_in,outfile):
    cfg,sh0 = work_00_merge(cfg_in)
    cfg,sh1 = work_01_pick_otu(cfg)
    cfg_alpha,sh_alpha = work_01_alpha_rare(cfg)

    group_list = re.split('\s+',cfg.get('all','group_names').strip())
    for group in cfg.get('all','group_names').strip():
        cfg_group,sh2 = work_02_otu_table(cfg)


    
