from settings import *

def data_merge(cfg_in,vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/data_merge.cfg')
    work.set_params(cfg_in,vars)
    work.load_default_config()

    config = work.config
    params = config.get_section('params')
    output = config.get_section('outfiles')
    scripts = config.get_section('scripts')
    work.commands.append('%s %s %s -f %s -s %s -r %s -n %s -d %s'%(scripts['00_Merge'],
                                                                   params['fq_for_merge'],
                                                                   output['out_dir'],
                                                                   output['fna_together'],
                                                                   output['fna_stat'],
                                                                   params['require'],
                                                                   params['name_list'],
                                                                   params['data_type']))

    work.write_config(output['out_dir'] + '/work.cfg')
    work.write_shell(output['out_dir'] + '/work.sh')

    return output

