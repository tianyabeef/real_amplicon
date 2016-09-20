#!/usr/bin/env python
# -*- coding: utf-8 -*- \#

from settings import *
from functional_modules import *
import time

PWD = os.getcwd()


def work_00(pipeline, infiles=None):
    outfiles = data_merge(pipeline.config)
    pipeline.make_shell(outfiles['out_dir'] + '/make.sh',
                        [('data_merge', outfiles['config'])])
    pipeline.add_job('data_merge', outfiles['shell'])
    return outfiles


def work_01(pipeline, infiles=None):
    vars = {
        'fna_file': infiles['fna_together'],
        'fna_stat': infiles['fna_stat'],
    }
    pick_otu_outfiles = pick_otu(pipeline.config, vars=vars)

    vars = {
        'work_dir': pick_otu_outfiles['out_dir'],
        'otu_mapping_file': pick_otu_outfiles['otus_all'],
        'reference_seqs': pick_otu_outfiles['seqs_all'],
    }
    otu_table_outfiles = make_otu_table(pipeline.config, vars=vars)

    #  vars = {
    #  'work_dir': pick_otu_outfiles['out_dir'],
    #  'otu_biom': otu_table_outfiles['otu_biom'],
    #  'stat_file': pick_otu_outfiles['out_stat_file'],
    #  'alpha_metrics': 'chao1,observed_species'
    #  }
    #  alpha_rare_outfiles = alpha_rare(pipeline.config, vars=vars)

    pipeline.make_shell(pick_otu_outfiles['out_dir'] + '/make.sh',
                        [('pick_otu', pick_otu_outfiles['config']),
                         ('make_otu_table', otu_table_outfiles['config'])])
    #  ('alpha_rare', alpha_rare_outfiles['config'])])
    pipeline.merge_shell(pick_otu_outfiles['out_dir'] + '/work.sh',
                         [pick_otu_outfiles['shell'],
                          otu_table_outfiles['shell']])
    #  alpha_rare_outfiles['shell']])
    pipeline.add_job('pick_otu',
                     pick_otu_outfiles['out_dir'] + '/work.sh',
                     prep='data_merge')
    pick_otu_outfiles['otu_biom'] = otu_table_outfiles['otu_biom']
    return pick_otu_outfiles


def total_alpha_rare(pipeline, infiles=None):
    vars = {
        'work_dir': infiles['out_dir'],
        'otu_biom': infiles['otu_biom'],
        'stat_file': infiles['out_stat_file'],
        'alpha_metrics': 'chao1,observed_species'
    }
    outfiles = alpha_rare(pipeline.config, vars=vars)
    pipeline.make_shell(outfiles['out_dir'] + '/make.sh',
                        [('alpha_rare', outfiles['config'])])
    pipeline.add_job('alpha_rare',
                     outfiles['shell'],
                     prep='pick_otu')


def work_02(pipeline, infiles=None):
    work_dir = pipeline.config.get('params', 'work_dir') + '/02_OTU_all'
    vars = {
        'work_dir': work_dir,
        'otu_table_in': infiles['otus_all'],
        'stat_file_in': infiles['out_stat_file'],
        'seqs_all': infiles['seqs_all'],
        'group': pipeline.config.get('params', 'alpha_group_file')
    }
    downsize_outfiles = downsize(pipeline.config, vars=vars)

    vars = {
        'work_dir': work_dir,
        'otu_mapping_file': downsize_outfiles['otu_table'],
        'reference_seqs': downsize_outfiles['seqs_fa']
    }
    otu_table_outfiles = make_otu_table(pipeline.config, vars=vars)

    vars = {
        'work_dir': work_dir,
        'otu_biom': otu_table_outfiles['otu_biom'],
        'uniform_profile': otu_table_outfiles['uniform_profile'],
        'tax_ass': otu_table_outfiles['tax_assign'],
        'total_group_file': pipeline.config.get('params', 'alpha_group_file')
    }
    taxanomy_total_outfiles = taxanomy_total(pipeline.config, vars=vars)

    pipeline.make_shell(work_dir + '/make.sh',
                        [('downsize', downsize_outfiles['config']),
                         ('make_otu_table', otu_table_outfiles['config']),
                         ('taxanomy_total', taxanomy_total_outfiles['config'])
                         ])
    pipeline.merge_shell(work_dir + '/work.sh',
                         [downsize_outfiles['shell'],
                          otu_table_outfiles['shell'],
                          taxanomy_total_outfiles['shell']])
    pipeline.add_job('OTU_all', work_dir + '/work.sh', prep='pick_otu')
    return otu_table_outfiles, downsize_outfiles['config']


def work_alpha_rare_all(pipeline, out_stat_file, infiles=None):
    work_dir = '%s/04_diversity_analysis/total_alpha_rare' % pipeline.config.get('params', 'work_dir')
    vars = {'work_dir': work_dir, 'rep_set': infiles['rep_set']}
    tree_outfiles = make_tree(pipeline.config, vars=vars)
    vars = {
        'work_dir': work_dir,
        'otu_biom': infiles['otu_biom'],
        'stat_file': out_stat_file,
        'tree_file': tree_outfiles['tree_file'],
        'choice_mode': 'MAX'
    }
    outfiles = alpha_rare(pipeline.config, vars=vars)
    pipeline.make_shell(work_dir + '/make.sh',
                        [('make_tree', tree_outfiles['config']),
                         ('alpha_rare', outfiles['config'])])
    pipeline.merge_shell(work_dir + '/work.sh', [tree_outfiles['shell'],
                                                 outfiles['shell']])

    pipeline.add_job('alpha_rare_all', work_dir + '/work.sh', prep='OTU_all')
    outfiles['tree_file'] = tree_outfiles['tree_file']
    return outfiles


def work_beta_anosim_adonis(pipeline, infiles=None, tree_file=None):
    work_dir = '%s/04_diversity_analysis/beta_ANOSIM_ADONIS' % pipeline.config.get('params', 'work_dir')
    vars = {
        'work_dir': work_dir,
        'otu_biom': infiles['otu_biom'],
        'tree_file': tree_file
    }
    outfiles = beta_ANOSIM_ADONIS(pipeline.config, vars=vars)
    pipeline.make_shell(work_dir + '/make.sh',
                        [('beta_ANOSIM_ADONIS', outfiles['config'])])
    pipeline.add_job('beta_anosim_adonis',
                     outfiles['shell'],
                     prep='alpha_rare_all')
    return outfiles


def work_03(pipeline, analysis_name, infiles=None, pre_config=None):
    work_dir = '%s/03_OTU_groups/%s' % (pipeline.config.get('params', 'work_dir'), analysis_name)
    vars = {
        'work_dir': work_dir,
        'otu_table_in': infiles['otus_all'],
        'stat_file_in': infiles['out_stat_file'],
        'seqs_all': infiles['seqs_all'],
        'group': infiles['group_file'],
        'pre_config': pre_config
    }
    downsize_outfiles = downsize(pipeline.config, vars=vars)

    vars = {
        'work_dir': work_dir,
        'otu_mapping_file': downsize_outfiles['otu_table'],
        'reference_seqs': downsize_outfiles['seqs_fa']
    }
    otu_table_outfiles = make_otu_table(pipeline.config, vars=vars)

    vars = {
        'work_dir': '%s/tax_rep_tree' % work_dir,
        'rep_set': otu_table_outfiles['tax_set'],
        'group': infiles['group_file'],
        'reference_seqs': downsize_outfiles['seqs_fa'],
        'otu_mapping_file': downsize_outfiles['otu_table'],
        'tax_assign': otu_table_outfiles['tax_assign'],
    }
    tax_rep_tree = make_tree(pipeline.config, vars=vars)

    vars = {
        'work_dir': work_dir,
        'group': infiles['group_file'],
        'otu_biom': otu_table_outfiles['otu_biom'],
        'uniform_profile': otu_table_outfiles['uniform_profile'],
        'tax_ass': otu_table_outfiles['tax_assign'],
        'newick': tax_rep_tree['tree_file'],
        'newicks': tax_rep_tree['tree_files'],
    }
    taxanomy_group_outfiles = taxanomy_group(pipeline.config, vars=vars)

    pipeline.make_shell(work_dir + '/make.sh',
                        [('downsize', downsize_outfiles['config']),
                         ('make_otu_table', otu_table_outfiles['config']),
                         ('make_tree', tax_rep_tree['config']),
                         ('taxanomy_total', taxanomy_group_outfiles['config']),
                         ])
    pipeline.merge_shell(work_dir + '/work.sh',
                         [downsize_outfiles['shell'],
                          otu_table_outfiles['shell'],
                          tax_rep_tree['shell'],
                          taxanomy_group_outfiles['shell'],
                          ])
    pipeline.add_job('OTU_group_' + analysis_name,
                     work_dir + '/work.sh',
                     prep='OTU_all')
    otu_table_outfiles['summarize_dir'] = taxanomy_group_outfiles['summarize_dir']
    return otu_table_outfiles


def work_diff(pipeline, analysis_name, group_file, infiles=None):
    work_dir = '%s/05_diff_analysis/%s' % (pipeline.config.get('params', 'work_dir'), analysis_name)
    vars = {
                'work_dir': work_dir,
                'group': group_file,
                'summarize_dir': infiles['summarize_dir'],
                'uniform_profile': infiles['uniform_profile']

            }
    try:
        if pipeline.config.get('params', 'abundance_cutoff'):
            abundance_cutoff = pipeline.config.get('params', 'abundance_cutoff')
            vars['abundance_cutoff'] = abundance_cutoff
    except:
        pass
    outfiles = taxanomy_diff(pipeline.config, vars=vars)
    pipeline.make_shell(work_dir + '/make.sh',
                        [('taxanomy_diff', outfiles['config'])])
    pipeline.add_job('diff_analysis_' + analysis_name,
                        outfiles['shell'],
                        prep='OTU_group_' + analysis_name)
    return outfiles




def work_tree(pipeline, analysis_name, infiles=None):
    work_dir = '%s/04_diversity_analysis/%s/tree' % (pipeline.config.get('params', 'work_dir'), analysis_name)
    vars = {'work_dir': work_dir, 'rep_set': infiles['rep_set']}
    outfiles = make_tree(pipeline.config, vars=vars)
    pipeline.make_shell(work_dir + '/make.sh',
                        [('make_tree', outfiles['config'])])
    pipeline.add_job('make_tree_' + analysis_name,
                     outfiles['shell'],
                     prep='OTU_group_' + analysis_name)
    return outfiles['tree_file']


def work_alpha_diversity(pipeline, analysis_name, tree_file, infiles=None):
    work_dir = '%s/04_diversity_analysis/%s/alpha' % (pipeline.config.get('params', 'work_dir'), analysis_name)
    vars = {
        'work_dir': work_dir,
        'alpha_group_file': infiles['group_file'],
        'stat_file': infiles['out_stat_file'],
        'tree_file': tree_file,
        'otu_biom': infiles['otu_biom'],
        'choice_mode': 'MAX'
    }
    alpha_rare_outfiles = alpha_rare(pipeline.config, vars=vars)

    vars = {
        'work_dir': work_dir,
        'group': infiles['group_file'],
        'alpha_div_collate_dir': alpha_rare_outfiles['alpha_collate_dir']
    }
    alpha_diversity_outfiles = alpha_diversity(pipeline.config, vars=vars)

    pipeline.make_shell(
            work_dir + '/make.sh',
            [('alpha_rare', alpha_rare_outfiles['config']),
             ('alpha_diversity', alpha_diversity_outfiles['config'])])
    pipeline.merge_shell(work_dir + '/work.sh',
                         [alpha_rare_outfiles['shell'],
                          alpha_diversity_outfiles['shell']])
    pipeline.add_job('alpha_div_' + analysis_name,
                     work_dir + '/work.sh',
                     prep="make_tree_" + analysis_name)
    return alpha_diversity_outfiles


def work_beta_diversity(pipeline, analysis_name, tree_file, infiles=None):
    work_dir = '%s/04_diversity_analysis/%s/beta' % (pipeline.config.get(
            'params', 'work_dir'), analysis_name)

    vars = {
        'work_dir': work_dir,
        'group': infiles['group_file'],
        'tree_file': tree_file,
        'otu_biom': infiles['otu_biom'],
        'stat_file': infiles['out_stat_file']
    }
    beta_diversity_outfiles = beta_diversity(pipeline.config, vars=vars)
    pipeline.make_shell(work_dir + '/make.sh',
                        [('beta_diversity', beta_diversity_outfiles['config'])
                         ])
    pipeline.add_job('beta_div_' + analysis_name,
                     beta_diversity_outfiles['shell'],
                     prep='make_tree_' + analysis_name)
    return beta_diversity_outfiles


def work_html(pipeline, group_files, infiles=None):
    word_dir = pipeline.config.get('params', 'work_dir')
    data_type = pipeline.config.get('params', 'data_type')
    job_id = pipeline.config.get('params', 'job_id')
    sequence_platform = pipeline.config.get('params', 'sequence_platform')
    # project information
    project_name = pipeline.config.get('project', 'project_name')
    customer_name = pipeline.config.get('project', 'customer_name')
    project_num = pipeline.config.get('project', 'project_num')
    sample_source = pipeline.config.get('project', 'sample_source')
    sample_type = pipeline.config.get('project', 'sample_type')
    note_information = pipeline.config.get('project', 'note_information')
    project_contacts = pipeline.config.get('project', 'project_contacts')
    phone = pipeline.config.get('project', 'phone')
    email = pipeline.config.get('project', 'email')
    enterprise_name = pipeline.config.get('project', 'enterprise_name')
    enterprise_address = pipeline.config.get('project', 'enterprise_address')
    salesman = pipeline.config.get('project', 'salesman')
    sale_phone = pipeline.config.get('project', 'sale_phone')
    sale_email = pipeline.config.get('project', 'sale_email')


    group_files = group_files
    work_dir = word_dir + "/" + job_id + "_report_" + time.strftime('%F') + "/"
    vars = {
        'work_dir': work_dir,
        'group_files': group_files,
        'data_type': data_type,
        'job_id': job_id,
        'project_name': project_name,
        'customer_name': customer_name,
        'project_num': project_num,
        'sample_source': sample_source,
        'sample_type': sample_type,
        'note_information': note_information,
        'project_contacts': project_contacts,
        'phone': phone,
        'email': email,
        'enterprise_name': enterprise_name,
        'enterprise_address': enterprise_address,
        'salesman': salesman,
        'sale_phone': sale_phone,
        'sale_email': sale_email,
        'sequence_platform':sequence_platform
    }
    get_result_outfile = get_result(pipeline.config, vars=vars)
    get_html_outfile = get_html(pipeline.config, vars=vars)

    rm_files = []
    rm_files.append(get_result_outfile['shell'])
    rm_files.append(get_result_outfile['config'])
    rm_files.append(get_html_outfile['shell'])
    rm_files.append(get_html_outfile['config'])
    rm_files.append(get_html_outfile['pdf_html'])
    rm_files.append('%s/templates' % (get_html_outfile['out_dir']))

    rm_shell = work_dir + '/clean.sh'
    with open(rm_shell, 'w') as out:
        out.write('rm -rf %s\n' % ' '.join(rm_files))

    pipeline.merge_shell(work_dir + '/work.sh', [get_result_outfile['shell'],
                                                 get_html_outfile['shell']])
    pipeline.add_job('html',
                     work_dir + '/work.sh',
                     prep=pipeline.html_hold_jobs[:-1])
    #  return rm_files


if __name__ == '__main__':
    work_cfg = PWD + '/work.cfg'
    pipeline = Pipeline(work_cfg)
    user_config = pipeline.config
    data_type = user_config.get('params', 'data_type')
    group_files = re.split('\s+', user_config.get('params', 'group_files'))

    outfiles_00 = work_00(pipeline)
    outfiles_01 = work_01(pipeline, infiles=outfiles_00)
    total_alpha_rare(pipeline, infiles=outfiles_01)
    outfiles_02, pre_config = work_02(pipeline, infiles=outfiles_01)
    alpha_outfiles_all = work_alpha_rare_all(pipeline,
                                             outfiles_01['out_stat_file'],
                                             infiles=outfiles_02)
    # beta_anosim_adonis = work_beta_anosim_adonis(
    #     pipeline,
    #     infiles=outfiles_02,
    #     tree_file=alpha_outfiles_all['tree_file'])
    for group_file in group_files:
        analysis_name = re.search('.+\/(.+)\..+', group_file).group(1)
        infiles = copy.deepcopy(outfiles_01)
        infiles['group_file'] = group_file
        outfiles_03 = work_03(pipeline, analysis_name, infiles=infiles, pre_config=pre_config)
        work_diff(pipeline, analysis_name, group_file, infiles=outfiles_03)
        tree_file = work_tree(pipeline, analysis_name, infiles=outfiles_03)
        infiles = {
            'group_file': group_file,
            'out_stat_file': infiles['out_stat_file'],
            'otu_biom': outfiles_03['otu_biom']
        }
        work_alpha_diversity(pipeline,
                             analysis_name,
                             tree_file,
                             infiles=infiles)
        work_beta_diversity(pipeline,
                            analysis_name,
                            tree_file,
                            infiles=infiles)
    work_html(pipeline, user_config.get('params', 'group_files'))
