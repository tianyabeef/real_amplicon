from __future__ import division
import re

class Group(object):

    def __init__(self,name):
        self.name = name
        self.samples = {}
        self.percent = {}
        self.other_percent = 0

    def get_percent(self,used_tax):
        self.sample_num = len(self.samples)
        for sample in self.samples.itervalues():
            for tax in used_tax:
                if tax not in self.percent:
                    self.percent[tax] = 0
                self.percent[tax] += sample.percent[tax] / self.sample_num
            self.other_percent += sample.other_percent / self.sample_num

class Sample(object):

    def __init__(self,name):
        self.name = name
        self.total_profile = 0
        self.tax = {}
        self.percent = {}
        self.other_percent = 0

    def pick_top(self,used_tax):
        other = 0
        uniform = 0
        for tax in self.tax.iterkeys():
            if tax in used_tax:
                self.percent[tax] = self.tax[tax] / self.total_profile * 100
                uniform += self.percent[tax]
            else:
                other += self.tax[tax]
        other = other / self.total_profile
        self.other_percent = other * 100
        uniform += self.other_percent


class Subject(object):

    def __init__(self,level,profile,outfile):
        self.sample = []
        self.level = level
        self.profile = profile
        self.outfile = outfile
        self.tax_total_profile = {}
        self.used_tax = []

    def read_profile(self):
        fp = open(self.profile)
        for line in fp:
            if line.startswith('# Constructed from'):
                continue
            if line.startswith('#'):
                self.get_samples(line)
            tax = line.strip().split('\t')[0]
            taxes = tax.split(';')
            for name in reversed(taxes):
                if re.search('^%s__'%self.level[0],name):
                    tax = name[3:]
                    break
            else:
                continue
            self.get_profile(tax,line)
        fp.close()

    def get_profile(self,tax,line):
        for ind,profile in enumerate(
                line.strip().split('\t')[1:]):
            self.sample[ind].tax[tax] = float(profile)
            self.sample[ind].total_profile += float(profile)
            if tax not in self.tax_total_profile:
                self.tax_total_profile[tax] = 0
            self.tax_total_profile[tax] += float(profile)

    def get_samples(self,header):
        for tab in header.strip().split('\t')[1:]:
            sample = Sample(tab)
            self.sample.append(sample)

    def pick_top(self):
        dict_ = self.tax_total_profile
        taxes_ = self.tax_total_profile.iterkeys()
        def my_cmp(a,b):
            n1 = dict_[a]
            n2 = dict_[b]
            return cmp(n2,n1)
        top = sorted(list(taxes_),
                cmp=my_cmp)[:20]
        self.used_tax = top

    def run(self,group=None):
        fp = open(self.outfile,'w')
        dict_ = self.tax_total_profile
        self.read_profile()
        self.pick_top()
        out_str = 'tax_name'
        sample_dict = {}
        for sample in self.sample:
            sample_dict[sample.name] = sample
        if group is not None:
            samples = list(group.iterkeys())
            samples = map(lambda s:sample_dict[s],samples)
        else:
            samples = self.sample
        for sample in samples:
            sample.pick_top(self.used_tax)
            out_str += '\t%s'%sample.name
        fp.write(out_str.strip() + '\n')
        for tax in sorted(self.used_tax,
                cmp=lambda a,b:cmp(dict_[b],dict_[a])):
            out_str = tax
            for sample in samples:
                out_str += '\t%s'%sample.percent[tax]
            fp.write(out_str.strip() + '\n')
        out_str = 'Other'
        for sample in samples:
            out_str += '\t%s'%sample.other_percent
        fp.write(out_str.strip() + '\n')
        fp.close()

    def run_with_group(self,group):
        fp = open(self.outfile,'w')
        dict_ = self.tax_total_profile
        self.read_profile()
        self.pick_top()
        out_str = 'tax_name'
        groups = {}
        for sample in self.sample:
            g = group[sample.name]
            if g not in groups:
                groups[g] = Group(g)
            groups[g].samples[sample.name] = sample
            sample.pick_top(self.used_tax)
        for g in groups.itervalues():
            g.get_percent(self.used_tax)
            out_str += '\t%s'%g.name
        fp.write(out_str.strip() + '\n')
        for tax in sorted(self.used_tax,
                cmp=lambda a,b:cmp(dict_[b],dict_[a])):
            out_str = tax
            for g in groups.itervalues():
                out_str += '\t%s'%g.percent[tax]
            fp.write(out_str.strip() + '\n')
        out_str = 'Other'
        for g in groups.itervalues():
            out_str += '\t%s'%g.other_percent
        fp.write(out_str.strip() + '\n')
        fp.close()

