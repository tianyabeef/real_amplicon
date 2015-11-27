#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import sys
from Parser import TableParser,TaxParser,parse_group_file

class Node(object):
    def __init__(self,level,name,samples,groups=None):
        self.sub_node = {}
        self.name = name
        self.level = level
        self.profile = {}
        for sample in samples:
            self.profile[sample] = 0
        if groups is not None:
            self.group_profile = {}
            for group in groups:
                self.group_profile[group] = 0


class Subject(object):

    def __init__(self,profile,taxfile,outfile,group_file=None,expand=1):
        self.table = TableParser(profile)
        self.otu_tax = TaxParser(taxfile)
        self.group = parse_group_file(group_file)
        if self.group is not None:
            self.groups = list(set(self.group.itervalues()))
        else:
            self.groups = None
        self.outfile = outfile
        self.expand = expand
        self.tax_level = ['kingdom','phylum','class','order','family','genus','species']
        self.tax_dict = {
            'k':'kingdom',
            'p':'phylum',
            'c':'class',
            'o':'order',
            'f':'family',
            'g':'genus',
            's':'species',
        }
        self.samples = {}
        self.node_list = {}
        self.root_nodes = {}

    def read_table(self):
        self.table.parse_table()
        self.table.get_uniform()
        self.samples = self.table.sample_list

    def read_tax(self):
        self.otu_tax.parse()
        self.otu_tax.remove_other()
        self.otu_tax = self.otu_tax.OTUs

    def get_tax_tree(self):
        for otu,otu_tax in self.otu_tax.iteritems():
            root_level = self.tax_level[0]
            father_level = root_level
            try:
                tax_name = otu_tax[root_level]
            except KeyError:
                if otu_tax:
                    print otu_tax
                    raise
                else:
                    continue
            if tax_name not in self.root_nodes:
                root_node = Node(root_level,tax_name,self.samples,groups=self.groups)
                self.node_list[tax_name] = root_node
                self.root_nodes[tax_name] = root_node
            levels = list(otu_tax.iterkeys())
            for ind,level in enumerate(levels):
                if level not in otu_tax:
                    continue
                father_node = self.node_list[otu_tax[father_level]]
                father_level = level
                tax_name = otu_tax[level]
                if tax_name in self.node_list:
                    continue
                node = Node(level,tax_name,self.samples,groups=self.groups)
                self.node_list[tax_name] = node
                if tax_name not in father_node.sub_node:
                    father_node.sub_node[tax_name] = node

    '''TODO:
        simplify beblow functions
    '''
    def get_node_profile(self,node):
        for sample in self.samples:
            for otu,otu_tax in self.otu_tax.iteritems():
                if node.level not in otu_tax or otu_tax[node.level] != node.name:
                    continue
                try:
                    node.profile[sample] += self.table.samples[sample][otu]
                except KeyError:
                    continue
        if not node.sub_node:
            return None
        for sub_node in node.sub_node.itervalues():
            self.get_node_profile(sub_node)

    def get_profile(self):
        for node in self.root_nodes.itervalues():
            self.get_node_profile(node)

    def get_node_group_profile(self,node):
        deleted = set()
        for sample,group in self.group.iteritems():
            for otu,otu_tax in self.otu_tax.iteritems():
                if node.level not in otu_tax or otu_tax[node.level] != node.name:
                    continue
                try:
                    node.group_profile[group] += self.table.samples[sample][otu]
                except KeyError,ex:
                    sample_name = str(ex).strip("'")
                    if sample_name not in deleted:
                        sys.stderr.write(sample_name)
                    deleted.add(sample_name)
                    continue
        for d in deleted:
            del self.group[d]
        if not node.sub_node:
            return None
        for sub_node in node.sub_node.itervalues():
            self.get_node_group_profile(sub_node)

    def get_group_profile(self):
        for node in self.root_nodes.itervalues():
            self.get_node_group_profile(node)

    def get_node_uniform(self,node):
        if not node.sub_node:
            return None
        for sample in self.samples:
            total = 0
            for sub_node in node.sub_node.itervalues():
                total += sub_node.profile[sample]
            if total == 0 or total == node.profile[sample]:
                continue
            for sub_node in node.sub_node.itervalues():
                sub_node.profile[sample] /= total
                sub_node.profile[sample] *= node.profile[sample]
        for sub_node in node.sub_node.itervalues():
            self.get_node_uniform(sub_node)

    def get_uniform(self,expand=1):
        for sample in self.samples:
            total = 0
            for node in self.root_nodes.itervalues():
                total += node.profile[sample]
            for node in self.root_nodes.itervalues():
                node.profile[sample] /= total
                node.profile[sample] *= expand
        for node in self.root_nodes.itervalues():
            self.get_node_uniform(node)

    def get_node_group_uniform(self,node):
        if not node.sub_node:
            return None
        for group in self.groups:
            total = 0
            for sub_node in node.sub_node.itervalues():
                total += sub_node.group_profile[group]
            if total == 0 or total == node.group_profile[group]:
                continue
            for sub_node in node.sub_node.itervalues():
                sub_node.group_profile[group] /= total
                sub_node.group_profile[group] *= node.group_profile[group]
        for sub_node in node.sub_node.itervalues():
            self.get_node_group_uniform(sub_node)

    def get_group_uniform(self,expand=1):
        for group in self.groups:
            total = 0
            for node in self.root_nodes.itervalues():
                total += node.group_profile[group]
            for node in self.root_nodes.itervalues():
                node.group_profile[group] /= total
                node.group_profile[group] *= expand
        for node in self.root_nodes.itervalues():
            self.get_node_group_uniform(node)


    def write_node(self,node,fp):
        level_name = self.tax_dict[node.name[0]]
        level_ind = self.tax_level.index(level_name)
        out_str = '\t'*level_ind + node.name[3:] + '\t'*(6-level_ind)
        for sample in self.samples:
            out_str += '\t%s'%node.profile[sample]
        fp.write(out_str + '\n')
        if not node.sub_node:
            return None
        for sub_node in node.sub_node.itervalues():
            self.write_node(sub_node,fp)

    def write_tree(self):
        with open(self.outfile,'w') as fp:
            fp.write('\t'.join(self.tax_level) + '\t' + '\t'.join(self.samples) + '\n')
            for node in self.root_nodes.itervalues():
                self.write_node(node,fp)

    def write_group_node(self,node,fp):
        level_name = self.tax_dict[node.name[0]]
        level_ind = self.tax_level.index(level_name)
        out_str = '\t'*level_ind + node.name[3:] + '\t'*(6-level_ind)
        for group in self.groups:
            out_str += '\t%s'%node.group_profile[group]
        fp.write(out_str + '\n')
        if not node.sub_node:
            return None
        for sub_node in node.sub_node.itervalues():
            self.write_group_node(sub_node,fp)

    def write_group_tree(self):
        with open(self.outfile,'w') as fp:
            fp.write('\t'.join(self.tax_level) + '\t' + '\t'.join(self.groups) + '\n')
            for node in self.root_nodes.itervalues():
                self.write_group_node(node,fp)

    def work(self):
        self.read_table()
        self.read_tax()
        self.get_tax_tree()
        if self.group is not None:
            self.get_group_profile()
            self.get_group_uniform(self.expand)
            self.write_group_tree()
        else:
            self.get_profile()
            self.get_uniform(self.expand)
            self.write_tree()
