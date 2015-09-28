from settings import *

def work_01_pick_otu(cfg_in):
    work = SubWork('01',cfg_in) 

    usearch = work.config.get('software','usearch')
    fna_file = work.config.get('all','fna_file')

    # get singleton reads
    out_dir = work.config.get('01','out_dir') + '/single'
    derep_fa = out_dir + '/derep.fa'
    singleton_stat = out_dir + '/stat.txt'
    work.commands.append('%s --infile %s --outdir %s'%(work.config.get('scripts','01_get_singleton_read'),fna_file,out_dir))

    # sort by size
    out_dir = work.config.get('01','out_dir')
    minsize = work.config.get('01','minsize')
    sorted_fa = out_dir + '/sorted.fa'
    work.commands.append('%s -sortbysize %s -output %s -minsize %s'%(usearch,derep_fa,sorted_fa,minsize))

    # cluster otus
    cluster_otus = out_dir + '/cluster_otus.fa'
    work.commands.append('%s -cluster_otus %s -otus %s'%(usearch,sorted_fa,cluster_otus))

    # rename
    otus_fa = out_dir + '/otus.fa'
    work.commands.append('%s --infile %s --outfile %s'%(work.config.get('scripts','01_rename_otu_fasta'),cluster_otus,otus_fa))

    # remap
    strand = work.config.get('01','strand')
    id = work.config.get('01','identity')
    map_uc = out_dir + '/map.uc'
    work.commands.append('%s -usearch_global %s -db %s -strand %s -id %s -uc %s'%(usearch,fna_file,otus_fa,strand,id,map_uc))

    # uc to otu_sample table 
    otus_tab = out_dir + '/otus_all.txt'
    work.commands.append('%s -i %s -o %s'%(work.config.get('scripts','01_uc2otutab'),map_uc,otus_tab))

    # otus_sample table to fa
    seqs_fa = out_dir + '/seqs_all.fa'
    work.commands.append('%s -i %s -t %s -o %s'%(work.config.get('scripts','01_otutab2fa'),fna_file,otus_tab,seqs_fa))
    
    # summary
    data_stat = work.config.get('00','data_stat for 01')
    out_stat_file = out_dir + '/pick_otu_summary.xls'
    work.commands.append('%s -r %s -s %s --uc %s -o %s'%(work.config.get('scripts','01_stat'),data_stat,singleton_stat,map_uc,out_stat_file)) 
    #work.commands.append('%s -r %s -s %s --otutab %s -o %s'%(work.config.get('scripts','01_stat'),data_stat,singleton_stat,otus_tab,out_stat_file))


    #set the output interface config
    work.config.set('01','otus_all',otus_tab)
    work.config.set('01','seqs_all',seqs_fa)
    work.config.set('01','stat_file',out_stat_file)

    # write
    work.write_config(out_dir + '/work.cfg')
    work.write_shell(out_dir + '/work.sh')

    return work.config,out_dir + '/work.sh'

def work_01_alpha_rare(cfg_in):
    work = SubWork('01',cfg_in)

    if  not work.config.has_option('01','otus_all') or not work.config.has_option('01','seqs_all'):
        sys.stderr.write('\nplease run pick otu first!\n')

    # get qiime 
    work.config.set_section('qiime',work.config.items('qiime'))

    out_dir = work.config.get('01','out_dir') + '/alpha_rare'

    # pick rep set
    rep_set = out_dir + '/rep_set.fna'
    work.commands.append('%s -i %s -f %s -o %s -m %s'%(work.config.get('qiime','pick_rep_set'),
                                                       work.config.get('01','otus_all'),
                                                       work.config.get('01','seqs_all'),
                                                       rep_set,
                                                       work.config.get('01','pick_rep_set_method')))

    # assign taxonomy
    classifier_file = out_dir + '/rdp_classifier.txt'
    hier_file = out_dir + '/rdp_hier.txt'
    tax_assign = out_dir + '/tax_assignment.txt'
    work.commands.append('%s -j %s -i %s -d %s -o %s -c %s --hier_outfile %s'%(work.config.get('scripts','01_rdp_classfier'),
                                                                   work.config.get('software','rdp_classifier'),
                                                                   rep_set,
                                                                   work.config.get('all','data_type'),
                                                                   classifier_file,
                                                                   work.config.get('01','classify_confident_cutoff'),
                                                                   hier_file))

    work.commands.append('%s -i %s -c %s -o %s'%(work.config.get('scripts','01_transform_rdp_qiime'),
                                                 classifier_file,
                                                 work.config.get('01','classify_confident_cutoff'),
                                                 tax_assign)) 

    # make otu table
    otu_biom = out_dir + '/otu_table.biom'
    work.commands.append('%s -i %s -t %s -o %s'%(work.config.get('qiime','make_otu_table'),
                                                 work.config.get('01','otus_all'),
                                                 tax_assign,
                                                 otu_biom))

    # multiple_rarefactions
    rarefaction_dir = out_dir + '/rarefaction'
    work.commands.append('%s -r %s -i %s -o %s -m %s -s %s -t %s'%(work.config.get('scripts','01_multiple_rarefactions'),
                                                                   work.config.get('qiime','multiple_rarefactions'),
                                                                   otu_biom,
                                                                   rarefaction_dir,
                                                                   work.config.get('01','rarefaction_min'),
                                                                   work.config.get('01','rarefaction_step'),
                                                                   work.config.get('01','stat_file')))
    # alpha diversity
    alpha_diversity_dir = out_dir + '/alpha_div'
    work.commands.append('%s -i %s -o %s --metrics %s'%(work.config.get('qiime','alpha_diversity'),
                                                        rarefaction_dir,
                                                        alpha_diversity_dir,
                                                        work.config.get('01','alpha_metrics')))

    # alpha collate
    alpha_collate_dir = out_dir + '/alpha_div_collated'
    work.commands.append('%s -i %s -o %s'%(work.config.get('qiime','collate_alpha'),
                                           alpha_diversity_dir,
                                           alpha_collate_dir))
    
    # alpha rare plot
    work.commands.append('%s -g %s -d %s -o %s -a %s'%(work.config.get('scripts','01_alpha_rare'),
                                                       work.config.get('all','total_group_file'),
                                                       alpha_collate_dir,
                                                       alpha_collate_dir,
                                                       work.config.get('01','alpha_metrics')))
    
    work.write_shell(out_dir + '/work.sh')
    work.write_config(out_dir + '/work.cfg')
    return work.config,out_dir + '/work.sh'


