from settings import *

def work_03_otu_analysis(cfg_in):
    work = SubWork('03',cfg_in)


    work.write_shell(out_dir + '/work.sh')
    work.write_config(out_dir + '/work.cfg')
    return work.config,out_dir + '/work.sh'

