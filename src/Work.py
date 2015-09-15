import sys
import os
import re
import ConfigParser as cp

class MyConfigParser(cp.SafeConfigParser):

    def __init__(self):
        cp.RawConfigParser.__init__(self)

    def optionxform(self,str):
        return str
    
    def add_section(self,section):
        try:
            cp.RawConfigParser.add_section(self,section)
        except cp.DuplicateSectionError,ex:
            return

    def set_section(self,section,items):
        self.add_section(section)
        for item in items:
            self.set(section,item[0],item[1])

    def add(self,section,name,value):
        if self.has_option(section,name):
            return
        else:
            self.add_section(section)
            self.set(section,name,value)

    def set(self,section,name,value):
        try:
            cp.RawConfigParser.set(self,section,name,value)
        except cp.NoSectionError,ex:
            self.add_section(section)
            cp.RawConfigParser.set(self,section,name,value)

class Work(object):
    def __init__(self):
        self.config = MyConfigParser()
        self.commands = []

    def read_config(self,config_file):
        config = MyConfigParser()
        config.readfp(open(config_file))
        self.config = config
        return config

    def write_config(self,out_file):
        out_dir = os.path.dirname(out_file)
        if not os.path.exists(out_dir):
            os.system('mkdir -p %s'%out_dir)
        fp = open(out_file,'w')
        self.config.write(fp)
        fp.close()

    def write_shell(self,shell_file):
        shell = open(shell_file,'w')
        shell.write("echo -e 'Begin at : \c' && date\n")
        for cmd in self.commands:
            shell.write(cmd + " && echo -e 'This-Work-is-Completed! : \c' && date\n")
        shell.write("echo -e 'All target finished at : \c' && date\n")
        shell.close()

class SubWork(Work):
    def __init__(self,work_id,cfg_in):
        if cfg_in.__class__ == str:
            cfg = MyConfigParser()
            cfg.readfp(open(cfg_in))
            cfg_in = cfg
        super(SubWork,self).__init__()
        self.work_id = work_id
        self.config.set_section('all',cfg_in.items('all'))
        self.config.set_section('software',cfg_in.items('software'))
        self.set_script(cfg_in)
        cfg_in.set(work_id,'work_dir',self.config.get('all','work_dir'))
        self.config.set_section(work_id,cfg_in.items(work_id))

    def set_script(self,cfg_in):
        for name,value in cfg_in.items('scripts'):
            if re.search('^%s'%self.work_id,name):
                self.config.set('scripts',name,value)

