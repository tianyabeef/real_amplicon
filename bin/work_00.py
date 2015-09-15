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

    # set the output interface config
    out_dir = work.config.get('00','out_dir')
    work.config.add('out_files','merged_file',out_dir + '/16S_together.fna')
    work.config.add('out_files','merged_stat',out_dir + '/16S_together.stat')
    work.config.add('out_files','work_shell',out_dir + '/work.sh')
    work.config.add('out_files','cfg_file',out_dir + '/work.cfg')
    work.config.set('all','fna_file',work.config.get('out_files','merged_file'))

    # set the commands
    script = work.config.get('scripts','00_merge')
    infile_list = work.config.get('00','fq_for_merge')
    out_dir = work.config.get('00','out_dir')
    require = work.config.get('00','require')
    name_table = work.config.get('00','name_table')
    work.commands.append('%s %s %s -r %s -n %s'%(script,infile_list,out_dir,require,name_table))

    # write
    work.config.remove_option('00','work_dir')
    work.write_config(work.config.get('out_files','cfg_file'))
    work.write_shell(work.config.get('out_files','work_shell'))

    return work.config

