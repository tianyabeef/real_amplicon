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

    return  outfiles

if __name__ == '__main__':
    config = sys.argv[1]
    pick_otu(config)
