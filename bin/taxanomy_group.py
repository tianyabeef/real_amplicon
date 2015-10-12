from settings import *

def taxanomy_group(cfg_in,vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/taxanomy_group.cfg')
    work.set_params(cfg_in,vars)
    work.load_default_config()

    config = work.config
    params = config.get_section('params')
    scripts = config.get_section('scripts')
    qiime = config.get_section('qiime')
    outfiles = config.get_section('outfiles')
    software = config.get_section('softwares')

    # summarize taxa
    work.commands.append('%s -i %s -o %s'%(qiime['summarize_taxa'],
                                           params['otu_biom'],
                                           outfiles['summarize_dir']))

    # core otu
    work.commands.append('%s -i %s -t %s -c %s -o %s'%(scripts['core_otu'],
                                                       params['uniform_profile'],
                                                       params['tax_ass'],
                                                       params['core_percent_cutoff'],
                                                       outfiles['core_otu_outdir']))
    

    return outfiles

if __name__ == '__main__':
    config = sys.argv[1]
    taxanomy_group(config)
