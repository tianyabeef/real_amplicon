#!/usr/bin/env python
from __future__ import division
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
    infile = open(infile)
    for record in SeqRecord.parse(infile,'fasta'):
        record.count = 1
        consumer.send(record)
    infile.close()
    return container

def containerClassfy(container):
    record = (yield )
    for index,ct_seq in enumerate(container):
        find_result = ct_seq.find_longer(record)
        if find_result:
            container[index] = find_result
            break
    else:
        container.append(record)

def write_container(container,outdir):
    out_single = open('%s/single.fa'%outdir,'w')
    out_rmsingle = open('%s/rm_single.fa'%outdir,'w')
    out_derep = open('%s/derep.fa'%outdir,'w')
    out_stat = open('%s/stat.txt'%outdir,'w')
    total_reads = 0
    single_reads = 0
    for index,ct_seq in enumerate(container):
        ct_seq.id = '%s;size=%s'%(ct_seq.id,ct_seq.count)
        total_reads += ct_seq.count
        if ct_seq.count == 1:
            out_single.write(ct_seq.format('fasta'))
            single_reads += 1
        else:
            out_rmsingle.write(ct_seq.format('fasta'))
        out_derep.write(ct_seq.format('fasta'))
    ratio = single_reads / total_reads * 100
    out_stat.write('total_reads\t%s\n'%total_reads)
    out_stat.write('single_reads\t%s\n'%single_reads)
    out_stat.write('single_ratio\t%2.2f%%\n'%ratio)
    out_derep.close()
    out_single.close()
    out_rmsingle.close()
    out_stat.close()

def get_read_hash(infile):
    read_hash = {}
    infile = open(infile)
    for record in SeqIO.parse(infile,'fasta'):
        read_hash[record.seq] = record
    infile.close()
    return read_hash

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(params['outdir']):
        os.mkdir(params['outdir']) 
    #read_hash = sorted(get_read_hash(params['infile']).iteritems(),key=lambda (k,v):len(k) )
    write_container(find_record(params['infile']),params['outdir'])

