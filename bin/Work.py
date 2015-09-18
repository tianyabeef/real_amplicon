import sys
import os
import re
import ConfigParser as cp

ENVIRONMENT = '''\
PYTHONPATH=''
R_HOME=/data_center_01/home/NEOLINE/liangzebin/soft/R/R-3.1.3
R_LIBS=$R_HOME/lib64/R/library
LD_LIBRARY_PATH=$R_HOME/lib:$LD_LIBRARY_PATH
PY_BIN=/data_center_01/home/liangzb/.pyenv/versions/2.7.10/bin
RDP_JAR_PATH=/home/snowflake/softwares/qiime/rdp_classifier_2.2/rdp_classifier-2.2.jar
LEfSe_PATH=/data_center_01/home/NEOLINE/liangzebin/soft/LEfSe/nsegata-lefse-094f447691f0
PATH=$PY_BIN:$R_HOME/bin:$LEfSe_PATH:$PATH

'''

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
        shell = open(shell_file,'w')
        shell.write('source /data_center_01/pipeline/16S_ITS_pipeline_v3.0/bin/environment.sh\n\n')
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
        self.cfg_in = cfg_in
        self.config.set_section('all',cfg_in.items('all'))
        self.config.set_section('software',cfg_in.items('software'))
        self.set_script()
        cfg_in.set(work_id,'work_dir',self.config.get('all','work_dir'))
        self.config.set_section(work_id,cfg_in.items(work_id))

    def set_script(self):
        for name,value in self.cfg_in.items('scripts'):
            if re.search('^%s'%self.work_id,name):
                self.config.set('scripts',name,value)

    def set_out_config(self):
        cfg_out = MyConfigParser()
        for section in self.config.sections():
            cfg_out.set_section(section,self.config.items(section))
        for section in self.cfg_in.sections():
            cfg_out.add_section(section,self.cfg_in.items(section,raw=True))
        self.cfg_out = cfg_out


