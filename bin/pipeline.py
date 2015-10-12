from settings import *
import argparse
from functional_modules import *

PWD = os.getcwd()

def work_00(pipeline,infiles=None):
    outfiles = data_merge(pipeline.config)
    pipeline.make_shell(outfiles['out_dir'] + '/make.sh',
                        [('data_merge',outfiles['config'])])
    pipeline.add_job('data_merge',outfiles['shell'])
    return outfiles

def work_01(pipeline,infiles=None):
    vars = {'fna_file':infiles['fna_together'],
            'fna_stat':infiles['fna_stat'],}
    pick_otu_outfiles = pick_otu(pipeline.config,vars=vars)

    vars = {'work_dir':pick_otu_outfiles['out_dir'],
            'otu_mapping_file':pick_otu_outfiles['otus_all'],
            'reference_seqs':pick_otu_outfiles['seqs_all'],}
    otu_table_outfiles = make_otu_table(pipeline.config,vars=vars)

    vars = {'work_dir':pick_otu_outfiles['out_dir'],
            'otu_biom':otu_table_outfiles['otu_biom'],
            'stat_file':pick_otu_outfiles['out_stat_file'],
            'alpha_metrics':'chao1,observed_species'}
    alpha_rare_outfiles = alpha_rare(pipeline.config,vars=vars)

    pipeline.make_shell(pick_otu_outfiles['out_dir'] + '/make.sh',
                        [('pick_otu',pick_otu_outfiles['config']),
                         ('make_otu_table',otu_table_outfiles['config']),
                         ('alpha_rare',alpha_rare_outfiles['config'])])
    pipeline.merge_shell(pick_otu_outfiles['out_dir'] + '/work.sh',
                         [pick_otu_outfiles['shell'],
                          otu_table_outfiles['shell'],
                          alpha_rare_outfiles['shell']])
    pipeline.add_job('pick_otu',pick_otu_outfiles['out_dir'] + '/work.sh',prep='data_merge')
    return pick_otu_outfiles

def work_02(pipeline,infiles=None):
    work_dir = pipeline.config.get('params','work_dir') + '/02_OTU_all'
    vars={'work_dir':work_dir,
          'otu_table_in':infiles['otus_all'],
          'stat_file_in':infiles['out_stat_file'],
          'seqs_all':infiles['seqs_all']}
    downsize_outfiles = downsize(pipeline.config,vars=vars)

    vars={'work_dir':work_dir,
          'otu_mapping_file':downsize_outfiles['otu_table'],
          'reference_seqs':downsize_outfiles['seqs_fa']}
    otu_table_outfiles = make_otu_table(pipeline.config,vars=vars)

    vars={'work_dir':work_dir,
          'otu_biom':otu_table_outfiles['otu_biom'],
          'uniform_profile':otu_table_outfiles['uniform_profile'],
          'tax_ass':otu_table_outfiles['tax_assign']}
    taxanomy_total_outfiles = taxanomy_total(pipeline.config,vars=vars)

    pipeline.make_shell(work_dir + '/make.sh',
                        [('downsize',downsize_outfiles['config']),
                         ('make_otu_table',otu_table_outfiles['config']),
                         ('taxanomy_total',taxanomy_total_outfiles['config'])])
    pipeline.merge_shell(work_dir + '/work.sh',
                         [downsize_outfiles['shell'],
                          otu_table_outfiles['shell'],
                          taxanomy_total_outfiles['shell']])
    pipeline.add_job('OTU_all',work_dir + '/work.sh',prep='pick_otu')
    return otu_table_outfiles

def work_03(pipeline,infiles=None):
    analysis_name = re.search('.+\/(.+)\..+',infiles['group_file']).group(1)
    work_dir = '%s/03_OTU_groups/%s'%(pipeline.config.get('params','work_dir'),analysis_name)
    vars={'work_dir':work_dir,
          'otu_table_in':infiles['otus_all'],
          'stat_file_in':infiles['out_stat_file'],
          'seqs_all':infiles['seqs_all'],
          'group':infiles['group_file']}
    downsize_outfiles = downsize(pipeline.config,vars=vars)

    vars={'work_dir':work_dir,
          'otu_mapping_file':downsize_outfiles['otu_table'],
          'reference_seqs':downsize_outfiles['seqs_fa']}
    otu_table_outfiles = make_otu_table(pipeline.config,vars=vars)
    
    vars={'work_dir':work_dir,
          'group':infiles['group_file'],
          'otu_biom':otu_table_outfiles['otu_biom'],
          'uniform_profile':otu_table_outfiles['uniform_profile'],
          'tax_ass':otu_table_outfiles['tax_assign']} 
    taxanomy_group_outfiles = taxanomy_group(pipeline.config,vars=vars)

    pipeline.make_shell(work_dir + '/make.sh',
                        [('downsize',downsize_outfiles['config']),
                         ('make_otu_table',otu_table_outfiles['config']),
                         ('taxanomy_total',taxanomy_group_outfiles['config'])])
    pipeline.merge_shell(work_dir + '/work.sh',
                         [downsize_outfiles['shell'],
                          otu_table_outfiles['shell'],
                          taxanomy_group_outfiles['shell']])
    pipeline.add_job('OTU_group',work_dir + '/work.sh',prep='pick_otu')
    return otu_table_outfiles

if __name__ == '__main__':

    work_cfg = PWD + '/work.cfg'

    pipeline = Pipeline(work_cfg)
    user_config = pipeline.config
    group_files = re.split('\s+',user_config.get('params','group_files'))

    outfiles_00 = work_00(pipeline)
    outfiles_01 = work_01(pipeline,infiles=outfiles_00) 
    outfiles_02 = work_02(pipeline,infiles=outfiles_01)
    for group_file in group_files:
        infiles = copy.deepcopy(outfiles_01)
        infiles['group_file'] = group_file
        outfiles_03 = work_03(pipeline,infiles)


