from settings import *

def check_group_row(file1,file2):
    count1 = []
    count2 = []
    with open(file1) as fp, open(file2) as fp2:
        for line in fp:
            sample_name = line.split('\t')[0]
            count1.append(sample_name)
        for line in fp2:
            sample_name = line.split('\t')[0]
            count2.append(sample_name)
    count1.sort()
    count2.sort()
    if count1 == count2:
        return True
    else:
        return False

def downsize(cfg_in,vars=None):
    work = Work(DEFAULT_CONFIG_DIR + '/downsize.cfg')
    work.set_params(cfg_in,vars)
    work.load_default_config()

    config = work.config
    params = config.get_section('params')
    scripts = config.get_section('scripts')
    outfiles = config.get_section('outfiles')

    flag = True
    if params['pre_config']:
        pre_config = MyConfigParser()
        pre_config.readfp(open(params['pre_config']))
        pre_outfiles = pre_config.get_section('outfiles')
        pre_group = pre_config.get('params','group')
        if check_group_row(pre_group,params['group']):
            work.commands.append('ln -s %s %s'%(pre_outfiles['otu_table'],outfiles['otu_table']))
            work.commands.append('ln -s %s %s'%(pre_outfiles['seqs_fa'],outfiles['seqs_fa']))
            work.commands.append('ln -s %s %s'%(pre_outfiles['downsize_stat'],outfiles['downsize_stat']))
            flag = False
    if flag:
        params['group'] = params['group'] or None

        if re.search('[t,y]',params['keep_small_size'].lower()):
            keep_small_size = '--keep_small_size'
        else:
            keep_small_size = '--no_keep_small_size'
        command = '%s -i %s -o %s --out_statfile %s %s' % (scripts['downsize'],
                                                           params['otu_table_in'],
                                                           outfiles['otu_table'],
                                                           outfiles['downsize_stat'],
                                                           keep_small_size)
        if params['minimum']:
            command += ' -m %s' % params['minimum']
        else:
            command += ' -s %s' % params['stat_file_in']
        if params['group']:
            command += '-g %s'%params['group']
        work.commands.append(command)

        work.commands.append('%s -i %s -t %s -o %s'%(scripts['otutab2fa'],
                                                    params['seqs_all'],
                                                    outfiles['otu_table'],
                                                    outfiles['seqs_fa']))

    return outfiles
