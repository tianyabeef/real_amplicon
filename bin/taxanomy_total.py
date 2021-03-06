from settings import *


def taxanomy_total(cfg_in, vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/taxanomy_total.cfg')
    work.set_params(cfg_in, vars)
    work.load_default_config()

    config = work.config
    params = config.get_section('params')
    scripts = config.get_section('scripts')
    qiime = config.get_section('qiime')
    outfiles = config.get_section('outfiles')

    sample_num_in_groups, \
    min_sample_num_in_groups, \
    sample_num_total, \
    group_num = parse_group(params['total_group_file'])

    # summarize taxa
    work.commands.append('%s -i %s -o %s' % (qiime['summarize_taxa'],
                                             params['otu_biom'],
                                             outfiles['summarize_dir']))

    # specaccum
    work.commands.append('%s -i %s -o %s' % (scripts['specaccum'],
                                             params['uniform_profile'],
                                             outfiles['specaccum_dir']))

    # rank_abundance
    work.commands.append('%s -s %s -i %s -o %s' % (scripts['rank_abundance'],
                                                   qiime['plot_rank_abundance_graph'],
                                                   params['otu_biom'],
                                                   outfiles['rank_abundance_dir']))

    # tax_star
    work.commands.append('%s -t %s -i %s -o %s -s %s' % (scripts['tax_star'],
                                                         params['tax_ass'],
                                                         params['uniform_profile'],
                                                         outfiles['tax_star_dir'],
                                                         params['total_group_file']))

    # bar_plot
    work.commands.append('%s -t %s -o %s -g %s' % (scripts['sample_bar_plot'],
                                                   outfiles['summarize_dir'],
                                                   outfiles['bar_plot_dir'],
                                                   params['total_group_file']))

    # bar_plot_contains_other
    work.commands.append('%s -t %s -o %s -g %s --contains_other' % (scripts['sample_bar_plot'],
                                                   outfiles['summarize_dir'],
                                                   outfiles['bar_plot_contains_other_dir'],
                                                   params['total_group_file']))



    # heatmap
    if sample_num_total >= 5:
        work.commands.append('%s -i %s -g %s -o %s -t %s' % (scripts['tax_heatmap'],
                                                             outfiles['summarize_dir'] + '/otu_table_L6.txt',
                                                             params['total_group_file'],
                                                             outfiles['tax_heatmap_outdir'],
                                                             params['heatmap_top']))
    return outfiles


if __name__ == '__main__':
    config = sys.argv[1]
    taxanomy_total(config)
