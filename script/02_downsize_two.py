#!/usr/bin/env python
import sys
import argparse
import os
from util import mkdir
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/../src')
#from Downsize import Subject
from Parser import parse_stat_file,parse_group_file


def read_params(args):
    parser = argparse.ArgumentParser(description='''downsize script | v1.0 at 2015/09/28 by liangzb ''')
    parser.add_argument('-o','--otu_table',dest='otu_table',metavar='file',type=str,required=True,
            help="otu_table file")
    #parser.add_argument('-s','--seqs_fa',dest='seqs_fa',metavar='file',type=str,required=True,
    #        help="seqs_fa original")
    parser.add_argument('-d','--downsize_stat',dest='downsize_stat',metavar='STR',type=str,required=True,
            help="downsize_stat original")
    parser.add_argument('-oo','--out_otu_table',dest='out_otu_table',metavar='OUTFILE',type=str,required=True,
            help="set the output file")
    #parser.add_argument('-os',dest='out_seqs_fa',metavar='FILE',type=str,required=True,
    #        help="set the stat file")
    parser.add_argument('-od',dest='out_downsize_stat',metavar='FILE',type=str,required=True,
                        help="downfile")
    parser.add_argument('-g',dest='group',metavar='FILE',type=str,required=True,
                        help="groupfile")
    args = parser.parse_args()
    params = vars(args)
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    otu_table = params["otu_table"]
    downsize_stat = params["downsize_stat"]
    out_otu_table = params["out_otu_table"]
    out_downsize_stat = params["out_downsize_stat"]
    group = params["group"]
    sample_list = []
    with open(group,mode="r") as fq:
        for line in fq:
            tabs  = line.strip().split("\t")
            sample_list.append(tabs[0])
    #print sample_list
    with open(otu_table,mode="r") as fq , open(downsize_stat,mode="r") as fq3 ,open(out_otu_table,mode="w") as fqout , open(out_downsize_stat,mode="w") as fqout3:
        for line in fq:
            tabs = line.strip().split("\t")
            tmp = []
            for value in tabs:
                if value.split("_")[0] in sample_list:
                    tmp.append(value)
     #       print "%s\t%s"%(tabs[0],len(tmp))
            if len(tmp)!=0:
                fqout.write("%s\t" % tabs[0])
                fqout.write("%s\n" % ("\t".join(tmp)))
        head = fq3.next()
        fqout3.write(head)
        for line in fq3:
            if line.strip().split("\t")[0] in sample_list:
                fqout3.write(line)




