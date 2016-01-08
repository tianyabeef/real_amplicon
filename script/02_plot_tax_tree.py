#!/data_center_01/home/liangzb/.pyenv/versions/anaconda-2.2.0/bin/python
# -*- coding: utf-8 -*- \#
"""
@author = 'liangzb'
@date = '2015-12-30'
This create newick format from qiime tax assignment file and otu profile
"""

from __future__ import division
import os
import sys
import argparse
import numpy as np
import pandas as pd
from collections import OrderedDict
from ete3 import Tree, TreeStyle, NodeStyle, TextFace
from util import LEVELS, TAX_DICT, SEARCH_REG, COLS_BREWER, float_trans, mkdir, image_trans

this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
from TaxTree import Tree as TaxTree
from TaxTree import TreeNode as Node

COLOR_DICT = OrderedDict()
for ind, level in enumerate(LEVELS):
    COLOR_DICT[level] = COLS_BREWER[ind % 20]


def read_params(args):
    parser = argparse.ArgumentParser(description='plot tax tree| v1.0 at 2015/01/06 by liangzb')
    parser.add_argument('--profile', dest='profile', metavar='FILE', type=str, required=True,
                        help="set the profile file")
    parser.add_argument('--tax_ass', dest='tax_ass', metavar='FILE', type=str, required=True,
                        help="set the tax_assignment.txt")
    parser.add_argument('--top', dest='top', metavar='INT', type=int, default=10,
                        help="set the top num, [default is 10]")
    parser.add_argument('-o', '--outdir', dest='outdir', metavar='DIR', type=str, required=True,
                        help="set the outdir")

    args = parser.parse_args()
    params = vars(args)
    return params


def table_uniform(table):
    for col_name, col in table.iteritems():
        table[col_name] = col.map(lambda s: s / col.sum())
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
    level_profile = otu_profile.loc[level.index]
    level_profile.index = level
    result = {}
    for p in level_profile.index.unique():
        if level_profile.loc[p].__class__ == pd.DataFrame:
            s = level_profile.loc[p].sum()
            s.name = p
        else:
            s = level_profile.loc[p]
        result[p] = s
    result = pd.DataFrame(result).T
    return result


def pick_high_abundance(level, otu_profile, top):
    def filter(n):
        if n in picked_level:
            return n
        else:
            return np.nan

    genus_profile = get_level_profile(otu_profile, level)
    genus_profile = genus_profile.T.sum()
    picked_level = genus_profile.sort(inplace=False)[:-top - 1:-1].index
    level = level.map(filter).dropna()
    return otu_profile.loc[level.index]


def read_profile(tax_ass, profile, top):
    tax_table = pd.DataFrame.from_csv(tax_ass, sep='\t', header=None)
    tax_table.columns = pd.Index(['tax_line', 'confidence'])
    tax_line = tax_table['tax_line']
    level_dict = {}
    for level in LEVELS:
        level_dict[level] = tax_line.map(get_tax(level=level)).dropna()
    otu_profile = pd.DataFrame.from_csv(profile, sep='\t')
    otu_profile = pick_high_abundance(level_dict['genus'], otu_profile, top)
    level_profile = {}
    total_profile = pd.DataFrame()
    for level in LEVELS:
        level_profile[level] = get_level_profile(otu_profile, level=level_dict[level]).dropna()
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


def read_tax(tax_ass, profile_dict):
    tree = TaxTree()
    with open(tax_ass) as fp:
        for line in fp:
            tabs = line.rstrip().split('\t')
            tax_line = tabs[1]
            tax_list = tax_line.split(';')
            for ind, tax_name in enumerate(tax_list):
                if tax_name not in profile_dict:
                    continue
                tax_level = TAX_DICT[tax_name[0]]
                if tax_name not in tree.nodes:
                    tree.nodes[tax_name] = Node(level=tax_level, name=tax_name)
                node_present = tree.nodes[tax_name]
                if ind > 0:
                    node_previous = tree.nodes[tax_list[ind - 1]]
                else:
                    node_previous = tree.root
                node_previous.add_child(child=node_present)
                node_present.profile = profile_dict[node_present.name]
                node_present.tree = tree
    return tree


def get_tree_style():
    ts = TreeStyle()
    # ts.mode = 'c'
    ts.margin_top = 10
    ts.margin_bottom = 10
    ts.margin_left = 10
    ts.margin_right = 10
    ts.show_leaf_name = False
    ts.show_branch_length = False
    ts.show_branch_support = False
    ts.show_scale = False
    title = TextFace("     Tax Assignment Tree", fsize=10)
    title.hz_align = 2
    title.vt_align = 2
    ts.scale = 1
    ts.title.add_face(TextFace(" "), column=0)
    ts.title.add_face(TextFace(" "), column=0)
    ts.title.add_face(title, column=0)
    return ts


def set_node_style(tree, node_dict, ts):
    root_node = tree & 'root'
    for node in tree.traverse():
        if node is root_node:
            node.set_style(NodeStyle(size=0))
            continue
        nstyle = NodeStyle()
        nstyle["shape"] = "circle"
        nstyle["size"] = node_dict[node.name].size
        try:
            nstyle["fgcolor"] = COLOR_DICT[node_dict[node.name].level]
        except KeyError:
            nstyle["fgcolor"] = "grey"
        nstyle["hz_line_type"] = 3
        nstyle["hz_line_color"] = "black"
        nstyle["hz_line_width"] = 1
        nstyle["vt_line_color"] = "black"
        nstyle["vt_line_width"] = 1
        node.set_style(nstyle)
        T1 = TextFace(node.name, ftype="Monaco", fsize=10)
        T1.hz_align = 0
        node.add_face(T1, 0, 'branch-top')
        T2 = TextFace(float_trans(node_dict[node.name].profile), ftype="Monaco", fsize=10)
        T2.hz_align = 0
        node.add_face(T2, 0, 'branch-bottom')
        node.dist = node_dict[node.name].branch_length


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['outdir'])
    modified_tax = '%s/tax_ass_modified.txt' % params['outdir']
    newick_file = '%s/tax_tree.nwk' % params['outdir']
    modify_tax_ass(params['tax_ass'], modified_tax)
    level_profile, total_profile = read_profile(modified_tax, params['profile'], params['top'])
    tree = read_tax(modified_tax, total_profile.T.mean())
    tree.adjust_profile()
    with open(newick_file, 'w') as out:
        out.write(str(tree))
    t = Tree(newick_file, format=1)
    ts = get_tree_style()
    set_node_style(t, tree.nodes, ts)

    pdf_file = '%s/tax_tree.pdf' % params['outdir']
    png_file = '%s/tax_tree.png' % params['outdir']
    t.render(pdf_file, tree_style=ts, dpi=100)
    image_trans(pdf_file, png_file)
