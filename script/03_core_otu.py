#!/usr/bin/env python
import sys
import argparse
import os
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/../src')
import RParser as rp

def read_params(args):
    parser = argparse.ArgumentParser(description='''core otu analysis | v1.0 at 2015/09/29 by liangzb ''')
    parser.add_argument('infile_list',metavar='INFILE_LIST',nargs='+',type=str,
            help="set your infile(s)")
    args = parser.parse_args()
    params = vars(args)
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(params['upload_dir']):
        os.mkdir(params['upload_dir'])

