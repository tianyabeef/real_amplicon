from settings import *

def make_otu_table(cfg_in,vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/make_otu_table.cfg')
    work.set_params(cfg_in,vars)
    work.load_default_config()

    config = work.config
    params = config.get_section('params')
    outfiles = config.get_section('outfiles')
    qiime = config.get_section('qiime')
    scripts = config.get_section('scripts')
    software = config.get_section('softwares')

    # intermediate result
    out_dir = outfiles['out_dir']
    rep_set = out_dir + '/rep_set.fna'
    classifier_file = out_dir + '/rdp_classifier.txt'
    tax_assign = out_dir + '/tax_assignment.txt'
    otu_biom = out_dir + '/otu_table.biom'

    # pick rep set
    work.commands.append('%s -i %s -f %s -o %s -m %s'%(qiime['pick_rep_set'],
                                                       params['otu_mapping_file'],
                                                       params['reference_seqs'],
                                                       rep_set,
                                                       params['pick_rep_set_method']))
    # assign taxonomy
    work.commands.append('%s -j %s -i %s -d %s -o %s -c %s --hier_outfile %s'%(scripts['rdp_classfier'],
                                                                               software['rdp_classifier'],
                                                                               rep_set,
                                                                               params['data_type'],
                                                                               classifier_file,
                                                                               params['classify_confident_cutoff'],
                                                                               out_dir + '/rdp_hier.txt'))
    work.commands.append('%s -i %s -c %s -o %s'%(scripts['transform_rdp_qiime'],
                                                 classifier_file,
                                                 params['classify_confident_cutoff'],
                                                 tax_assign))
    # make otu table
    work.commands.append('%s -i %s -t %s -o %s'%(qiime['make_otu_table'],
                                                 params['otu_mapping_file'],
                                                 tax_assign,
                                                 otu_biom))
    
    work.write_shell(outfiles['shell'])
    work.write_config(outfiles['config'])

    return outfiles
