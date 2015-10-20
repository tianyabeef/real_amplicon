import os
import re
import ConfigParser as cp


class MyConfigParser(cp.SafeConfigParser):

    def __init__(self):
        cp.RawConfigParser.__init__(self)

    def optionxform(self,str):
        return str

    def add_section(self,section,items=None):
        if items:
            if not self.has_section(section):
                self.add_section(section)
            for item in items:
                self.add(section,item[0],item[1])
        else:
            try:
                cp.RawConfigParser.add_section(self,section)
            except cp.DuplicateSectionError,ex:
                return

    def set_section(self,section,items=None):
        if items:
            if not self.has_section(section):
                self.add_section(section)
            for item in items:
                self.set(section,item[0],item[1])
        else:
            self.add_section(section)

    def get_section(self,section):
        var = {}
        for item in self.items(section):
            var[item[0]] = item[1]
        return var

    def add(self,section,name=None,value=None):
        if name:
            if self.has_option(section,name) and self.get(section,name) is not None:
                return
            else:
                self.set(section,name,value)
        else:
            self.add_section(section)

    def set(self,section,name=None,value=None):
        if name:
            try:
                cp.RawConfigParser.set(self,section,name,value)
            except cp.NoSectionError,ex:
                self.add_section(section)
                cp.RawConfigParser.set(self,section,name,value)
        else:
            self.add_sectioin(section)

    def rename(self,old,new):
        try:
            self.set_section(new,self.items(old))
        except cp.NoSectionError,ex:
            return False
        self.remove_section(old)

    def write(self,fp):
        try:
            cp.SafeConfigParser.write(self,fp)
        except cp.InterpolationMissingOptionError,ex:
            cp.RawConfigParser.write(self,fp)

class Work(object):

    def __init__(self,default_config):
        self.config = MyConfigParser()
        self.commands = []
        self.default_config = self.__read_config(default_config)

    def __del__(self):
        try:
            self.write_config(self.config.get('outfiles','config'))
            self.write_shell(self.config.get('outfiles','shell'))
        except cp.NoSectionError,ex:
            pass

    @staticmethod
    def __read_config(config):
        if config.__class__ == str:
            cfg = MyConfigParser()
            cfg.readfp(open(config))
            config = cfg
        return config

    def set_params(self,config,vars=None):
        params_list = self.default_config.options('params')
        config = self.__read_config(config)
        self.load_default_section('params')
        if config is None:
            return None
        try:
            param_dict = config.get_section('params')
        except cp.NoSectionError,ex:
            return None
        for option in params_list:
            try:
                self.config.set('params',option,param_dict[option])
            except KeyError,ex:
                if self.config.get('params',str(ex).strip("'")) is None:
                    raise KeyError,ex
        if vars is not None:
            for option,value in vars.iteritems():
                self.config.set('params',option,value)

    def set_config(self,config):
        config = self.__read_config(config)
        if config is None:
            return None
        for section in config.sections():
            self.config.set_section(section,items=config.items(section,raw=True))

    def load_default_section(self,section):
        _vars = None
        while 1:
            try:
                self.config.add_section(section,items=self.default_config.items(section,vars=_vars))
            except cp.InterpolationMissingOptionError,ex:
                if _vars is None:
                    _vars = {}
                _vars[ex.reference] = self.config.get('params',ex.reference)
            else:
                break
        if _vars is None:
            return
        for option in _vars.iterkeys():
            self.config.remove_option(section,option)

    def load_default_config(self):
        config = self.default_config
        if config is None or not config.sections():
            return None
        for section in config.sections():
            self.load_default_section(section)

    def write_config(self,out_file):
        out_dir = os.path.dirname(out_file)
        if not os.path.exists(out_dir):
            os.system('mkdir -p %s'%out_dir)
        fp = open(out_file,'w')
        self.config.write(fp)
        fp.close()

    def write_shell(self,shell_file):
        if not os.path.exists(os.path.dirname(shell_file)):
            os.system('mkdir -p %s'%os.path.dirname(shell_file))
        shell = open(shell_file,'w')
#        shell.write("echo -e 'Begin at : \c' && date\n")
        for cmd in self.commands:
            shell.write(cmd+'\n')
#            shell.write(cmd + " && echo -e 'This-Work-is-Completed! : \c' && date\n")
#        shell.write("echo -e 'All target finished at : \c' && date\n")
        shell.close()



class Pipeline(Work):

    def __init__(self,config):
        super(Pipeline,self).__init__(config)
        self.set_config(config)
        try:
            self.job_id = self.config.get('params','job_id')
        except cp.NoOptionError,ex:
            self.job_id = 'S'
        self.check_config()

    def check_config(self):
        params = self.get_section('params')
        assert params['data_type'] == '16S' or params['data_type'] == 'ITS'
        assert os.path.isdir(params['work_dir'])
        if params['fna_together']:
            assert os.path.isfile(params['fna_together'])
        for group_file in re.split('\s+',params['group_files']):
            assert os.path.isfile(group_file)
        if params['raw_data_dir']:
            assert os.path.isdir(params['raw_data_dir'])
        if params['fq_for_merge']:
            for file in params['fq_for_merge']:
                assert os.path.isfile(file)
        if params['name_list']:
            assert os.path.isfile(params['name_list'])

    @staticmethod
    def make_shell(work_shell,work_list):
        from settings import FUNCTIONAL_SCRIPT_DIR
        work_shell = open(work_shell,'w')
        for (work,config) in work_list:
            script = '%s/%s.py'%(FUNCTIONAL_SCRIPT_DIR,work)
            work_shell.write('python %s %s\n'%(script,config))
        work_shell.close()

    @staticmethod
    def merge_shell(total_shell,shell_list):
        total_shell = open(total_shell,'w')
        for shell in shell_list:
            total_shell.write('sh %s\n'%shell)
        total_shell.close()

    def add_job(self,job_name,shell,prep=None,vf='5G',queue='all.q'):
        qsub_name = '%s_%s'%(self.job_id,job_name)
        __o_file = '%s.o'%shell
        __e_file = '%s.e'%shell
        if os.path.isfile(__o_file):
            os.remove(__o_file)
        if os.path.isfile(__e_file):
            os.remove(__e_file)
        cmd = '%s=`qsub -cwd -l vf=%s -q %s -N %s -e %s -o %s -terse'%(job_name,vf,queue,qsub_name,
                                                                           __e_file,__o_file)
        if prep is not None:
            cmd += ' -hold_jid $%s'%prep
        cmd += ' %s`'%shell
        self.commands.append(cmd)

    def __del__(self):
        self.write_shell(self.config.get('params','pipeline_shell'))


class SubWork(Work):
    def __init__(self,work_id,cfg_in):
        if cfg_in.__class__ == str:
            cfg = MyConfigParser()
            cfg.readfp(open(cfg_in))
            cfg_in = cfg
        super(SubWork,self).__init__()
        self.work_id = work_id
        cfg_in.set(work_id,'work_dir',cfg_in.get('all','work_dir'))
        self.config = cfg_in



