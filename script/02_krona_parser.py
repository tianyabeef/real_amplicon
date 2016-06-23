#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"
import argparse
import os
import sys
import pandas as pd
def read_params(args):
    parser = argparse.ArgumentParser(description='group file change')
    parser.add_argument('-t', '--tax_assignment', dest='tax_assignment', metavar='tax_assignment', type=str, required=True,
                        help="16S produce tax_assignment.txt")
    parser.add_argument('-i', '--otu_table_uniform', dest='otu_table_uniform', metavar='otu_table_uniform', type=str, required=True,
                        help="16S produce otu_table_uniform.txt")
    parser.add_argument('-o', '--outputdir', dest='outputdir', metavar='outputdir', type=str, required=True,
                        help="out put dir")
    parser.add_argument('-r','--remove',dest='remove',action = 'store_true',default=False,help="remove txt files")
    args = parser.parse_args()
    params = vars(args)
    return params
if __name__ == '__main__':
    params = read_params(sys.argv)
    data = pd.DataFrame.from_csv(params["otu_table_uniform"],sep="\t")
    sample = data.columns
    outputdir = params["outputdir"]
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)
    for value in sample:
        with open(params["tax_assignment"],"r") as fq ,\
                open("%s/%s_for_krona.txt" % (outputdir,value),"w") as fqout:
            for line in fq:
                tabs = line.strip().split("\t")
                if float(data.loc[tabs[0],value])>0:
                    fqout.write("%s\t%s\n"%(data.loc[tabs[0],value],"\t".join(tabs[1].split(";"))))
        os.popen("perl /data_center_07/User/liangzb/soft/KronaTools/KronaTools-2.6/bin/ktImportText %s/%s_for_krona.txt -o %s/%s.html"%(outputdir,value,outputdir,value))
        if params["remove"]:
            os.popen("rm %s/%s_for_krona.txt"%(outputdir,value))
