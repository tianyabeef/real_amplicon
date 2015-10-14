from settings import *

def alpha_rare(cfg_in,vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/alpha_rare.cfg')
    work.set_params(cfg_in,vars)
    work.load_default_config()

    config = work.config
    params = config.get_section('params')
    outfiles = config.get_section('outfiles')
    qiime = config.get_section('qiime')
    scripts = config.get_section('scripts')

    out_dir = outfiles['out_dir']

    # multiple_rarefactions
    rarefaction_dir = out_dir + '/rarefaction'
    work.commands.append('%s -r %s -i %s -o %s -m %s -s %s -t %s'%(scripts['multiple_rarefactions'],
                                                                   qiime['multiple_rarefactions'],
                                                                   params['otu_biom'],
                                                                   rarefaction_dir,
                                                                   params['rarefaction_min'],
                                                                   params['rarefaction_step'],
                                                                   params['stat_file']))
    # alpha diversity
    alpha_diversity_dir = out_dir + '/alpha_div'
    work.commands.append('%s -i %s -o %s --metrics %s'%(qiime['alpha_diversity'],
                                                        rarefaction_dir,
                                                        alpha_diversity_dir,
                                                        params['alpha_metrics']))

    # alpha collate
    alpha_collate_dir = out_dir + '/alpha_div_collated'
    work.commands.append('%s -i %s -o %s'%(qiime['collate_alpha'],
                                           alpha_diversity_dir,
                                           alpha_collate_dir))

    # alpha rare plot
    work.commands.append('%s -g %s -d %s -o %s -a %s'%(scripts['alpha_rare'],
                                                       params['alpha_group_file'],
                                                       alpha_collate_dir,
                                                       alpha_collate_dir,
                                                       params['alpha_metrics']))

    return outfiles

if __name__ == '__main__':
    config = sys.argv[1]
    alpha_rare(config)

