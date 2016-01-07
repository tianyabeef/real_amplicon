#!/data_center_01/home/liangzb/.pyenv/versions/anaconda-2.2.0/bin/python
# -*- coding: utf-8 -*- \#
"""
@author = 'liangzb'
@date = '2015-12-30'
This create newick format from qiime tax assignment file and otu profile
"""

from __future__ import division
import sys
import argparse
from ete3 import Tree, TreeStyle, NodeStyle, TextFace, CircleFace
import pandas as pd
import numpy as np
import scipy as sp
from util import LEVELS, TAX_DICT, SEARCH_REG, float_trans, mkdir, image_trans


class Node(object):
    def __init__(self, level, name):
        self.node_father = None
        self.node_sub = {}
        self.name = name
        self.level = level

    def __str__(self):
        if self.node_sub:
            result = '('
            result += ','.join(map(str, self.node_sub.itervalues()))
            result += ')%s' % self.name
        else:
            result = self.name

        return result


NODE_ROOT = Node('root', 'root')


def read_params(args):
    parser = argparse.ArgumentParser(description='plot tax tree| v1.0 at 2015/01/06 by liangzb')
    parser.add_argument('--profile', dest='profile', metavar='FILE', type=str, required=True,
                        help="set the profile file")
    parser.add_argument('--tax_ass', dest='tax_ass', metavar='FILE', type=str, required=True,
                        help="set the tax_assignment.txt")
    parser.add_argument('-o', '--outdir', dest='outdir', metavar='DIR', type=str, required=True,
                        help="set the outdir")

    args = parser.parse_args()
    params = vars(args)
    return params


def table_uniform(table):
    for col_name, col in table.iteritems():
        table[col_name] = col.map(lambda s: sp.log10(s / col.sum() + 1))
    return table


def get_tax(level=None):
    def f(string):
        if level is None:
            return np.nan
        try:
            result = SEARCH_REG[level[0].lower()].search(string).group(1)
        except AttributeError:
            return np.nan
        return result

    return f


def get_level_profile(otu_profile, level):
    phylum_profile = otu_profile.loc[level.index]
    phylum_profile.index = level
    result = {}
    for p in phylum_profile.index.unique():
        if phylum_profile.loc[p].__class__ == pd.DataFrame:
            s = phylum_profile.loc[p].sum()
            s.name = p
        else:
            s = phylum_profile.loc[p]
        result[p] = s
    result = pd.DataFrame(result).T
    return result


def read_profile(tax_ass, profile):
    tax_table = pd.DataFrame.from_csv(tax_ass, sep='\t', header=None)
    tax_table.columns = pd.Index(['tax_line', 'confidence'])
    tax_line = tax_table['tax_line']
    level_dict = {}
    for level in LEVELS:
        level_dict[level] = tax_line.map(get_tax(level=level)).dropna()
    otu_profile = pd.DataFrame.from_csv(profile, sep='\t')
    level_profile = {}
    total_profile = pd.DataFrame()
    for level in LEVELS:
        level_profile[level] = get_level_profile(otu_profile, level=level_dict[level])
        level_profile[level] = table_uniform(level_profile[level])
        total_profile = pd.concat([total_profile, level_profile[level]])
    return level_profile, total_profile


def modify_tax_ass(tax_ass, outfile):
    with open(tax_ass) as fp, open(outfile, 'w') as out:
        for line in fp:
            tabs = line.rstrip().split('\t')
            tax_line = tabs[1]
            tax_list = tax_line.split(';')
            for ind, level in enumerate(LEVELS):
                try:
                    tax_name = tax_list[ind]
                except IndexError:
                    break
                if level[0] != tax_name[0]:
                    tax_list.insert(ind, '%s%s_unidentified' % (level[0], tax_name[1:13]))
            out.write('%s\t%s\t%s\n' % (tabs[0], ';'.join(tax_list), tabs[2]))


def read_tax(tax_ass):
    node_dict = {}
    with open(tax_ass) as fp:
        for line in fp:
            tabs = line.rstrip().split('\t')
            tax_line = tabs[1]
            tax_list = tax_line.split(';')
            for ind, tax_name in enumerate(tax_list):
                tax_level = TAX_DICT[tax_name[0]]
                if tax_name not in node_dict:
                    node_dict[tax_name] = Node(tax_level, tax_name)
                node_present = node_dict[tax_name]
                if ind > 0:
                    node_previous = node_dict[tax_list[ind - 1]]
                else:
                    node_previous = NODE_ROOT
                node_present.node_father = node_previous
                node_previous.node_sub[tax_name] = node_present
    return node_dict


def get_tree_style():
    ts = TreeStyle()
    ts.mode = 'c'
    ts.show_leaf_name = False
    ts.show_branch_length = False
    ts.show_branch_support = False
    ts.show_scale = False
    return ts


def set_node_style(tree, total_profile):
    sample_num = len(total_profile.columns)
    for node in tree.traverse():
        try:
            profile = total_profile.loc[node.name].sum() / sample_num
            print profile
        except KeyError:
            profile = 10 / 500
        nstyle = NodeStyle()
        nstyle["shape"] = "square"
        nstyle["size"] = 5
        nstyle["fgcolor"] = "red"
        nstyle["hz_line_type"] = 3
        nstyle["hz_line_color"] = "black"
        nstyle["hz_line_width"] = 5
        nstyle["vt_line_color"] = "black"
        nstyle["vt_line_width"] = 5
        node.set_style(nstyle)
        T1 = TextFace(node.name)
        T1.hz_align = 0
        node.add_face(T1, 0, 'branch-top')
        T2 = TextFace(float_trans(profile))
        T2.hz_align = 0
        node.add_face(T2, 0, 'branch-bottom')
        C = CircleFace(radius=profile * 500, color="RoyalBlue", style="sphere")
        C.opacity = 0.7
        C.hz_align = 0
        node.add_face(C, 0, 'float-behind')


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['outdir'])
    modified_tax = '%s/tax_ass_modified.txt' % params['outdir']
    modify_tax_ass(params['tax_ass'], modified_tax)
    node_dict = read_tax(params['tax_ass'])
    newick_file = '%s/tax_tree.nwk' % params['outdir']
    with open(newick_file, 'w') as out:
        out.write(str(NODE_ROOT) + ';')
    t = Tree(newick_file, format=1)
    level_profile, total_profile = read_profile(modified_tax, params['profile'])
    ts = get_tree_style()
    set_node_style(t, total_profile)

    pdf_file = '%s/tax_tree.pdf' % params['outdir']
    png_file = '%s/tax_tree.png' % params['outdir']
    t.render(pdf_file, tree_style=ts, dpi=300)
    image_trans(pdf_file, png_file)
