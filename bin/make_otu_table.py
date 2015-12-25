from settings import *


def make_otu_table(cfg_in, vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/make_otu_table.cfg')
    work.set_params(cfg_in, vars)
    work.load_default_config()

    config = work.config
    params = config.get_section('params')
    outfiles = config.get_section('outfiles')
    qiime = config.get_section('qiime')
    scripts = config.get_section('scripts')
    software = config.get_section('softwares')
    krona = config.get_section('krona')

    # intermediate result
    out_dir = outfiles['out_dir']
    classifier_file = out_dir + '/rdp_classifier.txt'

    # pick rep set
    work.commands.append('%s -i %s -f %s -o %s -m %s' % (qiime['pick_rep_set'],
                                                         params['otu_mapping_file'],
                                                         params['reference_seqs'],
                                                         outfiles['rep_set'],
                                                         params['pick_rep_set_method']))
    # assign taxonomy
    work.commands.append('%s -j %s -i %s -d %s -o %s -c %s --hier_outfile %s -m %s' % (scripts['rdp_classfier'],
                                                                                       software['rdp_classifier'],
                                                                                       outfiles['rep_set'],
                                                                                       params['data_type'],
                                                                                       classifier_file,
                                                                                       params[
                                                                                           'classify_confident_cutoff'],
                                                                                       out_dir + '/rdp_hier.txt',
                                                                                       params['rdp_memory']))
    work.commands.append('%s -i %s -c %s -o %s --rm_pollutes %s' % (scripts['transform_rdp_qiime'],
                                                                    classifier_file,
                                                                    params['classify_confident_cutoff'],
                                                                    outfiles['tax_assign'],
                                                                    params['pollutes']))
    work.commands.append('''less %s | perl -e 'print "otu_id\\ttax_name\\tconfidence\\n";while(<>){print;}' >%s''' % (
        outfiles['tax_assign'],
        outfiles['tax_assign_tsv']))
    # assign statistic
    work.commands.append('%s -i %s -t %s -o %s' % (scripts['otu_ass_stat'],
                                                   params['otu_mapping_file'],
                                                   outfiles['tax_assign'],
                                                   outfiles['tax_assign_stat']))
    # make otu table
    work.commands.append('%s -i %s -t %s -o %s' % (qiime['make_otu_table'],
                                                   params['otu_mapping_file'],
                                                   outfiles['tax_assign'],
                                                   outfiles['otu_biom']))
    # biom convert
    work.commands.append('%s -s %s -i %s -o %s' % (scripts['biom'],
                                                   software['biom'],
                                                   outfiles['otu_biom'],
                                                   outfiles['otu_txt']))
    # get uniform
    work.commands.append('%s -i %s -o %s' % (scripts['get_uniform'],
                                             outfiles['otu_txt'],
                                             outfiles['uniform_profile']))

    # get profile_tree
    work.commands.append('%s -i %s -t %s -o %s' % (scripts['profile_tree'],
                                                   outfiles['uniform_profile'],
                                                   outfiles['tax_assign'],
                                                   outfiles['profile_tree']))
    # get krona
    work.commands.append('perl %s %s -o %s' % (krona['ImportRDP'],
                                               classifier_file,
                                               outfiles['krona_html']))
    return outfiles


if __name__ == '__main__':
    config = sys.argv[1]
    make_otu_table(config)
