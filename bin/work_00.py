from settings import *

def work_00_merge(cfg_in):
    work = SubWork('00',cfg_in)
    ## make fq_for_merge option be relative path avaliable
    in_file_list = ' '
    for in_file in re.split('\s+',work.config.get('00','fq_for_merge').strip()):
        if re.search('\/',in_file.strip()):
            in_file_list += in_file + ' '
        else :
            in_file_list += work.config.get('00','raw_data_dir') + '/' + in_file + ' '
    work.config.set('00','fq_for_merge',in_file_list)

    # set the commands
    script = work.config.get('scripts','00_merge')
    infile_list = work.config.get('00','fq_for_merge')
    out_dir = work.config.get('00','out_dir')
    require = work.config.get('00','require')
    name_table = work.config.get('00','name_table')
    work.commands.append('%s %s %s -r %s -n %s'%(script,infile_list,out_dir,require,name_table))

    # write cfg and shell
    work.write_config(out_dir + '/work.cfg')
    work.write_shell(out_dir + '/work.sh')

    work.set_out_config()
    # set the output interface config
    data_type = work.config.get('all','data_type')
    work.cfg_out.set('00','data_stat for 01',out_dir + '/%s_together.stat'%data_type)
    work.cfg_out.set('all','fna_file',out_dir + '/%s_together.fna'%data_type)

    return work.cfg_out

