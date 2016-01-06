#!/data_center_01/home/liangzb/.pyenv/versions/anaconda-2.2.0/bin/python
# -*- coding: utf-8 -*- \#
"""
@author = 'liangzb'
@date = '2016-01-06'
plot phylo tree with newick and tax assign
"""
from __future__ import division
import re
import sys
import argparse
from collections import OrderedDict
from ete3.coretype.tree import TreeError
from ete3 import Tree, TreeStyle, NodeStyle
from ete3 import TextFace, faces, AttrFace, CircleFace
from util import cols_brewer, mkdir, image_trans


def read_params(args):
    parser = argparse.ArgumentParser(description='plot phylo tree with newick | v1.0 at 2015/01/06 by liangzb')
    parser.add_argument('--newick', dest='newick', metavar='FILE', type=str, required=True,
                        help="set the newick tree file")
    parser.add_argument('--tax_ass', dest='tax_ass', metavar='FILE', type=str, required=True,
                        help="set the tax_assignment.txt")
    parser.add_argument('-o', '--outdir', dest='outdir', metavar='DIR', type=str, required=True,
                        help="set the outdir")

    args = parser.parse_args()
    params = vars(args)
    return params


def get_dict(tax_ass):
    phylum_reg = re.compile('p__(.+)')
    genus_reg = re.compile('g__(.+)')
    genus_in_phylum = OrderedDict()
    phylum_genus = OrderedDict()
    with open(tax_ass) as fp:
        for line in fp:
            tabs = line.rstrip().split('\t')
            tax_line = tabs[1]
            taxes = tax_line.split(';')
            p = None
            g = None
            for tax in taxes:
                try:
                    p = phylum_reg.search(tax).group(1).replace(' ', '_')
                except AttributeError:
                    pass
                try:
                    g = genus_reg.search(tax).group(1).replace(' ', '_')
                except AttributeError:
                    pass
            if g is not None and p is not None:
                genus_in_phylum[g] = p
                phylum_genus[p] = g
    color_dict = OrderedDict()
    for ind, p in enumerate(list(phylum_genus.iterkeys())):
        color_dict[p] = cols_brewer[ind % 20]
    return color_dict, genus_in_phylum


def set_default_node_style(tree):
    # Draws nodes as small red spheres of diameter equal to 10 pixels
    nstyle = NodeStyle()
    nstyle["shape"] = "circle"
    nstyle["size"] = 10
    # nstyle["fgcolor"] = "red"

    # Gray dashed branch lines
    nstyle["hz_line_type"] = 3
    nstyle["hz_line_color"] = "black"
    nstyle["hz_line_width"] = 5
    nstyle["vt_line_color"] = "black"
    nstyle["vt_line_width"] = 5

    for node in tree.traverse():
        node.set_style(nstyle)


def get_default_tree_style(color_dict):
    ts = TreeStyle()
    ts.mode = 'c'
    # ts.layout_fn = layout
    ts.margin_top = 50
    ts.margin_bottom = 0
    ts.margin_left = 50
    ts.margin_right = 50
    ts.show_scale = False
    ts.show_leaf_name = False
    ts.show_branch_length = False
    ts.show_branch_support = False
    for p, c in color_dict.iteritems():
        ts.legend.add_face(TextFace("    ", fsize=30), column=0)
        ts.legend.add_face(CircleFace(10, c), column=1)
        ts.legend.add_face(TextFace("   %s" % p, fsize=30), column=2)
    legend_margin_line = 5
    while legend_margin_line:
        ts.legend.add_face(TextFace(" "), column=0)
        ts.legend.add_face(TextFace(" "), column=1)
        ts.legend.add_face(TextFace(" "), column=2)
        legend_margin_line -= 1
    ts.legend_position = 3
    return ts


def layout(node):
    if node.is_leaf():
        N = AttrFace("name", fsize=20)
        faces.add_face_to_node(N, node, 0, position="aligned")


def set_leaf_style(genus_in_phylum, tree):
    for leaf_name, phylum in genus_in_phylum.iteritems():
        time_redo = 2
        while time_redo:
            try:
                leaf = tree & leaf_name
                leaf_style = NodeStyle()
                leaf_style["shape"] = "circle"
                leaf_style["size"] = 10
                leaf_style["hz_line_type"] = 3
                leaf_style["hz_line_color"] = "black"
                leaf_style["hz_line_width"] = 5
                leaf_style["vt_line_color"] = "black"
                leaf_style["vt_line_width"] = 5
                bg_color = color_dict[phylum]
                leaf_style["bgcolor"] = bg_color
                leaf.set_style(leaf_style)
                leaf_face = TextFace(leaf_name.strip("'"), fsize=20)
                leaf.add_face(leaf_face, 0, 'aligned')
                break
            except TreeError:
                leaf_name = "'%s'" % leaf_name
                time_redo -= 1
                continue


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['outdir'])
    t = Tree(params['newick'], format=1)
    # t.show(tree_style=ts)
    color_dict, genus_in_phylum = get_dict(params['tax_ass'])
    set_default_node_style(t)
    set_leaf_style(genus_in_phylum, t)
    ts = get_default_tree_style(color_dict)

    pdf_file = '%s/phylo_tree.pdf' % params['outdir']
    png_file = '%s/phylo_tree.png' % params['outdir']
    t.render(pdf_file, tree_style=ts, dpi=300)
    image_trans(pdf_file, png_file)
