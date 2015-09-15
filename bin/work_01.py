from settings import *

def work_01_pick_otu(cfg_in):
    work = SubWork('01',cfg_in)

    # get singleton reads
    outdir = work.config.get('01','out_dir') + '/single')
    derep_fa = outdir + '/derep.fa'
    singleton_stat = outdir + '/stat.txt'
    work.commands.append('%s --infile %s --outdir %s'%(work.config.get('scripts','01_get_singleton_read'),
                                                       work.config.get('all','fna_file'),
                                                       singleton_outdir))

    # sort by size
    outdir = work.config.get('01','out_dir')
    usearch = work.config.get('software','usearch')
    minsize = work.config.get('01','minsize')
    sorted_fa = outdir + '/sorted.fa'
    work.commands.append('%s -sortbysize %s -output %s -minsize %s'%(usearch,derep_fa,sorted_fa,minsize))

    # cluster otus
    cluster_otus = outdir + '/cluster_otus.fa'
    work.commands.append('%s -cluster_otus %s -otus %s'%(usearch,sorted_fa,cluster_otus))

    # rename
    otus_fa = outdir + '/otus.fa'
    work.commands.append('%s --infile %s --outfile %s'%(work.config.get('scripts','01_rename_otu_fasta'),
                                                        cluster_otus,
                                                        otus_fa))

    # re map
    strand = work.config.get('01','strand')
    id = work.config.get('01','identity')
    map_uc = outdir + '/map.uc'
    work.commands.append('%s -usearch_global %s -db -strand %s -id %s -uc %s'%(usearch,
                                                                             work.config.get('all','fna_file'),
                                                                             strand,id,map_uc))

    # uc to otu sample table 
    otus_sample_table = out_dir + '/otus_all.txt'
    work.commands.append('%s -i %s -o %s'%(work.config.get('scripts','01_uc2otutab'),
                                           map_uc,otus_sample_table))


