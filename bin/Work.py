import sys
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

    def write(self,fp):
        try:
            cp.SafeConfigParser.write(self,fp)
        except cp.InterpolationMissingOptionError,ex:
            cp.RawConfigParser.write(self,fp)

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
        if not os.path.exists(os.path.dirname(shell_file)):
            os.system('mkdir -p %s'%os.path.dirname(shell_file))
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
        cfg_in.set(work_id,'work_dir',cfg_in.get('all','work_dir'))
        self.config = cfg_in
