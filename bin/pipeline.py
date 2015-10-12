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

def parse_group(group_file):
    sample_set = set()
    group_set = {}
    vars = {}
    with open(group_file) as group:
        for line in group:
            sample_name,group_name = line.strip().split('\t')
            if group_name not in group_set:
                group_set[group_name] = set()
            group_set[group_name].add(sample_name)
            sample_set.add(sample_name)
    sample_num_in_groups = map(lambda s:len(s),group_set)
    vars['min_sample_num_in_groups']= min(sample_num_in_groups)
    vars['sample_num_total'] = len(sample_set)
    vars['group_num'] = len(group_set)
    vars['analysis_name'] = re.search('.+\/(.+)\..+',group_file).group(1)
    return vars

def work_03(pipeline,in_vars=None):
    work_dir = '%s/03_OTU_groups/%s'%(pipeline.config.get('params','work_dir'),in_vars['analysis_name'])
    vars={'work_dir':work_dir,
          'otu_table_in':in_vars['otu_table_in'],
          'stat_file_in':in_vars['stat_file_in'],
          'seqs_all':in_vars['seqs_all'],
          'group':in_vars['group_file']}
    downsize_outfiles = downsize(pipeline.config,vars=vars)

    vars={'work_dir':work_dir,
          'otu_mapping_file':downsize_outfiles['otu_table'],
          'reference_seqs':downsize_outfiles['seqs_fa']}
    otu_table_outfiles = make_otu_table(pipeline.config,vars=vars)
    
    vars={'work_dir':work_dir,
          'group':in_vars['group_file'],
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
        vars = parse_group(group_file)
        vars['otu_table_in'] = outfiles_01['otus_all']
        vars['seqs_all'] = outfiles_01['seqs_all']
        vars['stat_file_in'] = outfiles_01['out_stat_file']
        vars['group_file'] = group_file
        outfiles_03 = work_03(pipeline,vars)


