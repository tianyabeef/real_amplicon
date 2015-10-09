from settings import *

def downsize(cfg_in,vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/downsize.cfg')
    work.set_params(cfg_in,vars)
    work.load_default_config()

    config = work.config
    params = config.get_section('params')
    scripts = config.get_section('scripts')
    outfiles = config.get_section('outfiles')

    work.commands.append('%s -s %s -i %s -o %s --out_statfile %s -k %s'%(scripts['downsize'],
                                                                           params['stat_file_in'],
                                                                           params['otu_table_in'],
                                                                           outfiles['otu_table'],
                                                                           outfiles['downsize_stat'],
                                                                           params['keep_small_size']))

    work.commands.append('%s -i %s -t %s -o %s'%(scripts['otutab2fa'],
                                                 params['seqs_all'],
                                                 outfiles['otu_table'],
                                                 outfiles['seqs_fa']))

    return outfiles 
