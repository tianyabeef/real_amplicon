#!/usr/bin/env python
# -*- coding:utf-8 -*- #
from settings import *


def get_command(rep_set_file, tree_file, params, scripts, qiime, outfiles):
    if params['data_type'] == '16S':
        command = "%s --align_seq_py %s --make_phylogeny_py %s " % (scripts['make_tree'],
                                                                qiime['align_seqs'],
                                                                qiime['make_phylogeny'])

        if not params['align_method']:
            params['align_method'] = 'pynast'
        command += '-i %s -a %s -d %s --tree_file %s -o %s ' % (rep_set_file,
                                                            params['align_method'],
                                                            params['data_type'],
                                                            tree_file,
                                                            outfiles['out_dir'])
        if params['align_method'] == 'pynast':
            if not params['pre_align']:
                raise IOError, 'must set the pre align file when align_method is pynast'
            command += "-t %s " % params['pre_align']
        if params['lanemask']:
            command += '--filter_alignment_py %s -m %s ' % (qiime['filter_alignment'],
                                                            params['lanemask'])

    elif params['data_type'] == 'ITS':
        command = "%s  --make_phylogeny_py %s " % (scripts['make_tree'],
                                                   qiime['make_phylogeny'])
        command += '-i %s -d %s --tree_file %s -o %s ' % (rep_set_file,
                                                            params['data_type'],
                                                            tree_file,
                                                            outfiles['out_dir'])
        command += '--retree %s --mafft %s ' % (params['retree'],
                                                            qiime['mafft'])
    return command


def make_tree(cfg_in, vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/make_tree.cfg')
    work.set_params(cfg_in, vars)
    work.load_default_config()

    config = work.config
    params = config.get_section('params')
    scripts = config.get_section('scripts')
    qiime = config.get_section('qiime')
    outfiles = config.get_section('outfiles')

    if params['group']:
        # pick rep set
        work.commands.append('%s --pick_rep_set %s -i %s -f %s -g %s -o %s -m %s' % (scripts['pick_rep_set'],
                                                                                     qiime['pick_rep_set'],
                                                                                     params['otu_mapping_file'],
                                                                                     params['reference_seqs'],
                                                                                     params['group'],
                                                                                     outfiles['rep_set_dir'],
                                                                                     params['pick_rep_set_method']))
        group = parse_group_file(params['group'])
        group_names = set(group.itervalues())
        for group_name in group_names:
            rep_set_file = '%s/%s.rep_set.fna' % (outfiles['rep_set_dir'], group_name)
            tax_set_file = '%s/%s.tax_set.fna' % (outfiles['rep_set_dir'], group_name)
            tree_file = '%s/%s.rep_phylo.tre' % (outfiles['out_dir'], group_name)
            outfiles['tree_files'] += ' %s' % tree_file
            work.commands.append('%s --rep_set %s --tax_ass %s -o %s' % (scripts['get_genus_rep'],
                                                                         rep_set_file,
                                                                         params['tax_assign'],
                                                                         tax_set_file))
            command = get_command(tax_set_file, tree_file, params, scripts, qiime, outfiles)
            work.commands.append(command)
        config.set('outfiles', 'tree_files', outfiles['tree_files'])

        # make tree
    command = get_command(params['rep_set'], outfiles['tree_file'], params, scripts, qiime, outfiles)
    work.commands.append(command)

    return outfiles


if __name__ == '__main__':
    config = sys.argv[1]
    make_tree(config)
