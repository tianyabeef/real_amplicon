from settings import *

def pick_otu(cfg_in,vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/pick_otu.cfg')
    work.set_params(cfg_in,vars)
    work.load_default_config()

    config = work.config
    usearch = config.get('softwares','usearch')
    params = config.get_section('params')
    scripts = config.get_section('scripts')
    outfiles = config.get_section('outfiles')

    # intermediate result
    out_dir = outfiles['out_dir']
    sorted_fa = out_dir + '/sorted.fa'
    cluster_otus = out_dir + '/cluster_otus.fa'
    otus_fa = out_dir + '/otus.fa'
    map_uc = out_dir + '/map.uc'

    # get singleton reads
    work.commands.append('%s --infile %s --outdir %s'%(scripts['01_get_singleton_read'],
                                                       params['fna_file'],
                                                       outfiles['single_dir']))
    # sort by size
    work.commands.append('%s -sortbysize %s -output %s -minsize %s'%(usearch,
                                                                      outfiles['single_dir'] + '/derep.fa',
                                                                      sorted_fa,
                                                                      params['minsize']))
    # cluster otus
    work.commands.append('%s -cluster_otus %s -otus %s'%(usearch,
                                                         sorted_fa,
                                                         cluster_otus))
    # rename
    work.commands.append('%s --infile %s --outfile %s'%(scripts['01_rename_otu_fasta'],
                                                        cluster_otus,
                                                        otus_fa))
    # remap
    work.commands.append('%s -usearch_global %s -db %s -strand %s -id %s -uc %s'%(usearch,
                                                                                  params['fna_file'],
                                                                                  otus_fa,
                                                                                  params['strand'],
                                                                                  params['identity'],
                                                                                  map_uc))
    # uc to otu_sample table 
    work.commands.append('%s -i %s -o %s'%(scripts['01_uc2otutab'],
                                           map_uc,
                                           outfiles['otus_all']))
    # otus_sample table to fa
    seqs_fa = out_dir + '/seqs_all.fa'
    work.commands.append('%s -i %s -t %s -o %s'%(scripts['01_otutab2fa'],
                                                 params['fna_file'],
                                                 outfiles['otus_all'],
                                                 outfiles['seqs_all']))
    # summary
    work.commands.append('%s -r %s -s %s --single_list %s --uc %s -o %s'%(scripts['01_stat'],
                                                                          params['fna_stat'],
                                                                          outfiles['single_dir'] + '/stat.txt',
                                                                          outfiles['single_dir'] + '/single.list',
                                                                          map_uc,
                                                                          outfiles['out_stat_file'])) 

    work.write_config(outfiles['config'])
    work.write_shell(outfiles['shell'])

    return  outfiles 

def work_01_alpha_rare(cfg_in):
    work = SubWork('01',cfg_in)

    if  not work.config.has_option('01','otus_all') or not work.config.has_option('01','seqs_all'):
        sys.stderr.write('\nplease run pick otu first!\n')

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


