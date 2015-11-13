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
    sample_num_in_groups,\
    min_sample_num_in_groups,\
    sample_num_total,\
    group_num = parse_group(params['group'])

    # summarize taxa
    work.commands.append('%s -i %s -o %s'%(qiime['summarize_taxa'],
                                           params['otu_biom'],
                                           outfiles['summarize_dir']))
    # summarize trans
    work.commands.append('%s -i %s'%(scripts['summarize_trans'],
                                     outfiles['summarize_dir']))

    # bar_plot
    work.commands.append('%s -t %s -o %s -g %s --with_group'%(scripts['group_bar_plot'],
                                                              outfiles['summarize_dir'],
                                                              outfiles['bar_plot_dir'],
                                                              params['group']))

    # core otu
    if sample_num_total >= 5:
        work.commands.append('%s -i %s -t %s -c %s -o %s'%(scripts['core_otu'],
                                                           params['uniform_profile'],
                                                           params['tax_ass'],
                                                           params['core_percent_cutoff'],
                                                           outfiles['core_otu_outdir']))

    # otu venn
    if group_num >= 2 and group_num <= 5:
        work.commands.append('%s -i %s -g %s -o %s'%(scripts['otu_venn'],
                                                     params['uniform_profile'],
                                                     params['group'],
                                                     outfiles['otu_venn_outdir']))
    # tax_pca
    if sample_num_total >= 5:
        work.commands.append('%s -i %s -g %s -o %s'%(scripts['otu_pca'],
                                                     params['uniform_profile'],
                                                     params['group'],
                                                     outfiles['otu_pca_outdir']))
    # heatmap
    if sample_num_total >= 5:
        work.commands.append('%s -i %s -g %s -o %s -t %s'%(scripts['tax_heatmap'],
                                                           outfiles['summarize_dir'] + '/otu_table_L6.txt',
                                                           params['group'],
                                                           outfiles['tax_heatmap_outdir'],
                                                           params['heatmap_top']))
    return outfiles

if __name__ == '__main__':
    config = sys.argv[1]
    taxanomy_group(config)
