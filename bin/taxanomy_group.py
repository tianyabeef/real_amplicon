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


    

    return outfile

if __name__ == '__main__':
    config = sys.argv[1]
    taxanomy_group(config)
