import os
from string import Template

class MyTemplate(Template):
    delimiter = '@#'

class Parser(object):
    def __init__(self):
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

def parse_stat_file(stat_file,group_file=None):
    used_samples = set()
    used_samples = set()
    if group_file is not None:
        with open(group_file) as g:
            for line in g:
                used_samples.add(line.split('\t')[0])
    with open(stat_file) as fp:
        line = fp.next()
        while(line):
            line = fp.next().strip()
        fp.next()
        maximum = 0
        minimum = 0xffffff
        for line in fp:
            tabs = line.strip().split('\t')
            if used_samples and tabs[0] not in used_samples:
                continue
            if maximum < int(tabs[1]):
                maximum = int(tabs[1])
            if minimum > int(tabs[2]):
                minimum = int(tabs[2])
    return maximum,minimum

def parse_group_file(file):
    group = {}
    with open(file) as g:
        for line in g:
            tabs = line.strip().split('\t')
            group[tabs[0]] = tabs[1]
    return group
