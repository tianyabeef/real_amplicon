#!/usr/bin/env python
import sys
import argparse
sys.path.insert(1,'../src')
from Bio import SeqIO
from MySeqRecord import SeqRecord

def read_params(args):
    parser = argparse.ArgumentParser(description='get singleton reads')
    parser.add_argument('-i',dest='infile',metavar='str',type=str,
            help="set your input file ")
    parser.add_argument('-o',dest='outdir',metavar='str',type=str,default='./single',
            help="set your output dir")

    args = parser.parse_args()
    params = vars(args)
    return params

def find_record(infile):
    container = []
    consumer = containerClassfy()
    consumer.next()
    for record in SeqRecord.parse(open(infile),'fasta'):
        consumer.send(record)
    return container

def containerClassfy(container):
    record = (yield )
    for index,ct_seq in enumerate(container):
        find_result = ct_seq.find_sub_seq(record)
        if find_result:
            container[index] = find_result
            break
    else:
        container.append(record)

        

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(params['outdir']):
        os.mkdir(params['outdir'])
    

