import os
from string import Template

class MyTemplate(Template):
    delimiter = '@#'

class RParser(object):
    def __init__(self,work_dir):
        self.work_dir = work_dir
        self.template = None
        self.R_script = None
        self.file = None

    def open(self,template):
        fp = open(template)
        template = fp.read()
        fp.close()
        self.template = MyTemplate(template)

    def format(self,var):
        self.R_script = self.template.safe_substitute(var)

    def write(self,outfile):
        fp = open(outfile,'w')
        fp.write(self.R_script)
        self.file = outfile
        fp.close()

    def run(self):
        os.system('R CMD BATCH --slave %(Rfile)s %(Rfile)sout'%{'Rfile':self.file})
