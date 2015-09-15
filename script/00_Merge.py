#!/usr/bin/env python
import sys
import argparse
import os
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/../src')
import Merge as mg

def read_params(args):
    parser = argparse.ArgumentParser(description='16S/ITS data merge')
    parser.add_argument('infile_list',metavar='INFILE_LIST',nargs='+',type=str,
            help="set your infile[s] ")
    parser.add_argument('outdir',metavar='OUTDIR',type=str,default='./',
            help="set your output dir")
    parser.add_argument('-r',dest='required',metavar='int',type=int,default=50000,
            help="set the required data of this subject")
    parser.add_argument('-n',dest='name_table',metavar='str',type=str,default=None,
            help="set the name convert table")

    args = parser.parse_args() 
    params = vars(args)
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    subject = mg.Subject(params['infile_list'],params['outdir'],params['required'],name_table_file=params['name_table'])
    subject.read_name_table()
    subject.merge()
    subject.write_stat()
