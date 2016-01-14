from settings import *


def taxanomy_group(cfg_in, vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/taxanomy_group.cfg')
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
    group_num = parse_group(params['group'])

    # summarize taxa
    work.commands.append('%s -i %s -o %s' % (qiime['summarize_taxa'],
                                             params['otu_biom'],
                                             outfiles['summarize_dir']))
    # summarize trans
    work.commands.append('%s -i %s' % (scripts['summarize_trans'],
                                       outfiles['summarize_dir']))

    # bar_plot
    work.commands.append('%s -t %s -o %s -g %s --with_group' % (scripts['group_bar_plot'],
                                                                outfiles['summarize_dir'],
                                                                outfiles['bar_plot_dir'],
                                                                params['group']))

    # core otu
    if sample_num_total >= 5:
        work.commands.append('%s -i %s -t %s -c %s -o %s' % (scripts['core_otu'],
                                                             params['uniform_profile'],
                                                             params['tax_ass'],
                                                             params['core_percent_cutoff'],
                                                             outfiles['core_otu_outdir']))

    # otu venn
    if group_num >= 2 and group_num <= 5:
        work.commands.append('%s -i %s -g %s -o %s' % (scripts['otu_venn'],
                                                       params['uniform_profile'],
                                                       params['group'],
                                                       outfiles['otu_venn_outdir']))
    elif group_num > 5:
        work.commands.append('%s %s %s %s' % (scripts['otu_flower'],
                                              params['uniform_profile'],
                                              params['group'],
                                              outfiles['otu_venn_outdir']))
    # tax_pca
    if sample_num_total >= 5:
        command = '%s -i %s -g %s -o %s' % (scripts['otu_pca'],
                                            params['uniform_profile'],
                                            params['group'],
                                            outfiles['otu_pca_outdir'])
        if min_sample_num_in_groups >= 5:
            command += ' --with_boxplot'
        else:
            command += ' --without_boxplot'
        work.commands.append(command)

    # heatmap
    if sample_num_total >= 5:
        work.commands.append('%s -i %s -g %s -o %s -t %s' % (scripts['tax_heatmap'],
                                                             outfiles['summarize_dir'] + '/otu_table_L6.txt',
                                                             params['group'],
                                                             outfiles['tax_heatmap_outdir'],
                                                             params['heatmap_top']))
    # tax tree
    work.commands.append('%s -i %s -g %s -o %s -t %s' % (scripts['tax_bar_tree'],
                                                         outfiles['summarize_dir'] + '/otu_table_L6.txt',
                                                         params['group'],
                                                         outfiles['tax_bar_tree_outdir'],
                                                         params['bar_tree_top']))

    # plot phylo tree
    work.commands.append('%s --newick %s --tax_ass %s -o %s' % (scripts['plot_phylo_tree'],
                                                                params['newick'],
                                                                params['tax_ass'],
                                                                outfiles['phylo_tree_outdir']))
    # plot tax tree
    command = '%s --profile %s --tax_ass %s --top %s -o %s' % (scripts['plot_tax_tree'],
                                                               params['uniform_profile'],
                                                               params['tax_ass'],
                                                               params['tax_tree_top'],
                                                               outfiles['tax_tree_outdir']
                                                               )
    # plot tax tree with branch circle
    work.commands.append('%s --with_branch_circle --plot_in_samples' % command)
    # plot tax tree with leaf pie
    work.commands.append('%s -g %s --with_leaf_pie' % (command, params['group']))
    return outfiles


if __name__ == '__main__':
    config = sys.argv[1]
    taxanomy_group(config)
