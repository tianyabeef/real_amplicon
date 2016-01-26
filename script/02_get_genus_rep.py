#!/usr/bin/env python
# -*- coding: utf-8 -*- \#
"""
@author = 'liangzb'
@date = '2016-01-06'
get genus rep from rep set and tax ass
"""

from __future__ import division
import re
import os
import sys
import argparse
from util import mkdir
from Bio import SeqIO


def read_params(args):
    parser = argparse.ArgumentParser(description='get genus rep | v1.0 at 2015/01/06 by liangzb')
    parser.add_argument('--rep_set', dest='rep_set', metavar='FILE', type=str, required=True,
                        help="set the rep_set.fna")
    parser.add_argument('--tax_ass', dest='tax_ass', metavar='FILE', type=str, required=True,
                        help="set the tax_assignment.txt")
    parser.add_argument('-o', '--outfile', dest='outfile', metavar='FILE', type=str, required=True,
                        help="set the output tax_rep.fna")

    args = parser.parse_args()
    params = vars(args)
    return params


def get_genus(tax_ass):
    genus_reg = re.compile('g__([^;]+)')
    genus = {}
    genus_values = set()
    with open(tax_ass) as fp:
        for line in fp:
            tabs = line.rstrip().split('\t')
            try:
                g = genus_reg.search(tabs[1]).group(1)
            except AttributeError:
                continue
            g = g.replace(' ', '_')
            if g not in genus_values:
                genus[tabs[0]] = g
                genus_values.add(g)
    return genus


def output(tax_rep, rep_set, genus):
    with open(tax_rep, 'w') as out:
        for record in SeqIO.parse(open(rep_set), 'fasta'):
            record.description = record.id
            try:
                record.id = genus[record.id]
            except KeyError:
                continue
            out.write(record.format('fasta'))


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(os.path.dirname(params['outfile']))
    genus = get_genus(params['tax_ass'])
    output(params['outfile'], params['rep_set'], genus)
