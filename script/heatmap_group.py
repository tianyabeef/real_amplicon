#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

import sys
import argparse
import re
def read_params(args):
    parser = argparse.ArgumentParser(description='a wrapper for rdp classify | v1.0 at 2015/09/18 by liangzb')
    parser.add_argument('-i', '--infile', dest='infile', metavar='FILE', type=str, required=True,
                        help="set the input file ")
    parser.add_argument('-t', '--taxfile', dest='taxfile', metavar='FILE', type=str, required=True,
                        help="set the input taxanomy file")
    parser.add_argument('-inl', '--inputlevel', dest='inputlevel', metavar='inputlevel', type=str,default="g__",
                        help="default [g__]")
    parser.add_argument('-o', '--outfile', dest='outfile', metavar='FILE', type=str, required=True,
                        help="set the output file")
    parser.add_argument('-ol', '--outlevel', dest='outlevel', metavar='outlevel', type=str, default="p__",
                        help="[ default p__ ]")
    args = parser.parse_args()
    params = vars(args)
    return params


if __name__ == '__main__':
    params = read_params(sys.argv)
    infile = params["infile"]
    outfile = params["outfile"]
    inlevel = params["inputlevel"]
    outlevel = params["outlevel"]
    taxfile = params["taxfile"]
    search_name = {}
    with open(infile,"r") as fq:
        for line in fq:
            name = line.strip()
            name = "%s%s" % (inlevel,name)
            search_name[name] = ""
    with open(taxfile,'r') as fq:
        for line in fq:
            if line.startswith("#"):
                continue
            tabs = line.strip().split("\t")
            tabs = tabs[0].split(";")
            for value in tabs:
                if value.find(outlevel)==0:
                    outlevel_name = value
                if search_name.has_key(value):
                    search_name[value] = outlevel_name
    with open(outfile,"w") as fqout:
        for key,value in search_name.items():
            fqout.write("%s\t%s\n" %(key.split("__")[1],value.split("__")[1]))

