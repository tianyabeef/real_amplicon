import random
import re

class Reads(object):

    def __init__(self,id,otu_name):
        self.name = id
        self.id = re.search('(\d+)$',id).group(1)
        self.otu_name = otu_name
        self.sample_name = re.search('(.*)_\d+$',id).group(1)

class Sample(object):

    def __init__(self,name):
        self.name = name
        self.total_num = 0
        self.used_num = 0
        self.otu_before = set()
        self.otu_final = set()

class OTU(object):

    def __init__(self,name):
        self.name = name
        self.reads = []

    def __str__(self):
        if not self.reads:
            return ''
        out_str = self.name + '\t'
        for read in self.reads:
            out_str += read.name + '\t'
        return out_str.strip() + '\n'

class Subject(object):

    def __init__(self,infile,outfile,statfile,
                 minimum,
                 group,
                 keep=True,
                 random=True):
        self.infile = infile
        self.outfile = outfile
        self.statfile = statfile
        self.minimum = minimum
        self.keep = keep
        self.group = group
        self.random = random
        self.sample_dict = {}
        self.reads = []
        self.otu_dict = {}

    def count_stat(self):
        fp = open(self.infile)
        for line in fp:
            tabs = line.strip().split('\t')
            otu_name = tabs.pop(0)
            self.otu_dict[otu_name] = OTU(otu_name)
            for tab in tabs:
                read = Reads(tab,otu_name)
                if read.sample_name not in self.group:
                    continue
                if read.sample_name not in self.sample_dict:
                    sample = Sample(read.sample_name)
                    self.sample_dict[read.sample_name] = sample
                sample = self.sample_dict[read.sample_name]
                sample.total_num += 1
                sample.otu_before.add(otu_name)
                self.reads.append(read)
        fp.close()

    @staticmethod
    def my_cmp(a,b):
        if a.sample_name > b.sample_name:
            return 1
        elif a.sample_name < b.sample_name:
            return -1
        else:
            return cmp(a.id,b.id)

    def get_downsize(self):
        if self.random:
            random.shuffle(self.reads)
        else:
            self.reads.sort(cmp=self.my_cmp)
        for read in self.reads:
            sample = self.sample_dict[read.sample_name]
            otu = self.otu_dict[read.otu_name]
            if not self.keep and sample.total_num < self.minimum:
                continue
            if sample.used_num >= self.minimum:
                continue
            sample.used_num += 1
            sample.otu_final.add(read.otu_name)
            otu.reads.append(read)

    def output(self):
        fp = open(self.outfile,'w')
        for otu in self.otu_dict.itervalues():
            fp.write(str(otu))
        fp.close()

    def writestat(self):
        fp = open(self.statfile,'w')
        fp.write('sample_name\teven_reads_num\totu_num_before\totu_num_final\n')
        for sample_name in sorted(list(self.sample_dict.iterkeys())):
            sample = self.sample_dict[sample_name]
            fp.write('%s\t%s\t%s\t%s\n'%(sample_name,
                                         sample.used_num,
                                         len(sample.otu_before),
                                         len(sample.otu_final)))
        fp.close()

    def work(self):
        self.count_stat()
        self.get_downsize()
        self.output()
        if self.statfile is not None:
            self.writestat()

