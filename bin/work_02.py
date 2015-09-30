from settings import *

def work_02_otu_table(cfg_in):
    work = SubWork('02',cfg_in)

    # downsize
    out_dir = work.config.get('02','out_dir')
    downsize_table = out_dir + '/otu_downsized.txt'
    otu_downsize_stat = out_dir + '/otu_downsize_stat.xls'
    work.commands.append('%s -s %s -i %s -o %s --out_statfile %s -k True'%(work.config.get('scripts','02_downsize'),
                                                                           work.config.get('01','stat_file'),
                                                                           work.config.get('01','otus_all'),
                                                                           downsize_table,
                                                                           otu_downsize_stat))

    # downsize otu to fa
    downsize_fa = out_dir + '/seqs_downsized.fa'
    work.commands.append('%s -i %s -t %s -o %s'%(work.config.get('scripts','01_otutab2fa'),
                                                 work.config.get('01','seqs_all'),
                                                 downsize_table,
                                                 downsize_fa))

    # pick rep seq
    rep_set = out_dir + '/rep_set.fa'
    work.commands.append('%s -i %s -f %s -o %s -m %s'%(work.config.get('qiime','pick_rep_set'),
                                                       downsize_table,
                                                       downsize_fa,
                                                       rep_set,
                                                       work.config.get('02','pick_rep_set_method')))
    
    # assign taxonomy
    classifier_file = out_dir + '/rdp_classifier.txt'
    hier_file = out_dir + '/rdp_hier.txt'
    tax_assign = out_dir + '/tax_assignment.txt'
    work.commands.append('%s -j %s -i %s -d %s -o %s -c %s --hier_outfile %s'%(work.config.get('scripts','01_rdp_classfier'),
                                                                               work.config.get('software','rdp_classifier'),
                                                                               rep_set,
                                                                               work.config.get('all','data_type'),
                                                                               classifier_file,
                                                                               work.config.get('02','classify_confident_cutoff'),
                                                                               hier_file))

    work.commands.append('%s -i %s -c %s -o %s'%(work.config.get('scripts','01_transform_rdp_qiime'),
                                                 classifier_file,
                                                 work.config.get('02','classify_confident_cutoff'),
                                                 tax_assign))

    # make otu table
    otu_biom = out_dir + '/otu_table.biom'
    work.commands.append('%s -i %s -t %s -o %s'%(work.config.get('qiime','make_otu_table'),
                                                 downsize_table,
                                                 tax_assign,
                                                 otu_biom))

    # summarize taxa
    summarize_out_dir = out_dir + '/wf_taxa_summary'
    work.commands.append('%s -i %s -o %s'%(work.config.get('qiime','summarize_taxa'),
                                           otu_biom,
                                           summarize_out_dir))

    # biom convert
    otu_txt = out_dir + '/otu_table.txt'
    work.commands.append('%s -s %s -i %s -o %s'%(work.config.get('scripts','02_biom'),
                                                 work.config.get('software','biom'),
                                                 otu_biom,
                                                 otu_txt))

    # get uniform
    uniform_profile = out_dir + '/otu_table_uniform.txt'
    work.commands.append('%s -i %s -o %s'%(work.config.get('scripts','02_get_uniform'),
                                           otu_txt,
                                           uniform_profile))

    work.config.set('02','otu_table',otu_txt)
    work.config.set('02','otu_table_profile',uniform_profile)
    work.config.set('02','otu_biom',otu_biom)
    work.config.set('02','taxa_summary_dir',summarize_out_dir)
    work.config.set('02','otu_downsize_stat',otu_downsize_stat)
    work.write_shell(out_dir + '/work.sh')
    work.write_config(out_dir + '/work.cfg')
    return work.config,out_dir + '/work.sh'


