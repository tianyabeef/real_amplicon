from __future__ import division
import re

class OTU(object):
    def __init__(self,name,tax_level,tax_name):
        self.name = name
        self.tax_level = tax_level
        self.tax_name = tax_name
        self.percent = 0

class Subject(object):
    tax_level = ['kingdom','phylum','class','order','family','genus','specie']
    tax_level_dic = {'k':'kingdom','p':'phylum','c':'class',
                     'o':'order','f':'family','g':'genus','s':'specie'}

    def __init__(self,otu_table,tax_ass,for_plot,core_txt,cutoff):
        self.otu_table = otu_table
        self.tax_ass = tax_ass
        self.cutoff = cutoff
        self.for_plot = for_plot
        self.core_txt = core_txt
        self.otus = {}

    def work(self):
        self.get_tax_ass()
        self.read_otu_table()
        self.write_for_plot()
        self.write_core_otu()

    def get_tax_ass(self):
        with open(self.tax_ass) as tax_ass:
            for line in tax_ass:
                otu,tax,conf = line.strip().split('\t')
                tax = tax.split(';')[-1]
                tax_short,tax_name = re.search('(\w)__(.+)',tax).groups()
                tax_level = self.tax_level_dic[tax_short]
                self.otus[otu] = OTU(otu,tax_level,tax_name)

    def read_otu_table(self):
        with open(self.otu_table) as table:
            head = table.next()
            if head.startswith('# Constructed from'):
                head = table.next()
            for line in table:
                tabs = line.strip().split('\t')
                otu = self.otus[tabs.pop(0)]
                n = 0
                for tab in tabs:
                    if float(tab) > 0:
                        n += 1
                otu.percent = n / len(tabs)

    def write_for_plot(self):
        self.segments = {}
        segs = ['>0.5','>0.6','>0.7','>0.8','>0.9','==1']
        for s in segs:
            self.segments[s] = 0
        for otu in self.otus.itervalues():
            p = otu.percent
            for s in segs:
                if eval('%s%s'%(p,s)):
                    self.segments[s] += 1
        with open(self.for_plot,'w') as for_plot:
            for s in segs:
                for_plot.write('%s\t%s\n'%(s,self.segments[s]))
                if not eval('%s%s'%(self.cutoff,s)):
                    break

    def write_core_otu(self):
        with open(self.core_txt,'w') as core_otu:
            core_otu.write('OTU ID\tTaxonomy\tname\n')
            for otu in self.otus.itervalues():
                if otu.percent >= self.cutoff:
                    core_otu.write('%s\t%s\t%s'%(otu.name,otu.tax_level,otu.tax_name))
