from settings import *
import argparse
from work_00 import data_merge
from work_01 import pick_otu
from make_otu_table import make_otu_table

PWD = os.getcwd()

if __name__ == '__main__':

    work_cfg = PWD + '/work.cfg'

    pipeline = Pipeline(work_cfg)
    user_config = pipeline.config

    data_merge_outfiles = data_merge(user_config)
    pipeline.add_job('data_merge',data_merge_outfiles['shell'])

    vars = {'fna_file':data_merge_outfiles['fna_together'],
            'fna_stat':data_merge_outfiles['fna_stat'],}
    pick_otu_outfiles = pick_otu(user_config,vars=vars)

    vars = {'work_dir':pick_otu_outfiles['out_dir'],
            'otu_mapping_file':pick_otu_outfiles['otus_all'],
            'reference_seqs':pick_otu_outfiles['seqs_all'],}
    otu_table_outfiles = make_otu_table(user_config,vars=vars)

    

    
    
