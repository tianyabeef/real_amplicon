from __future__ import division
import sys
import os
import re
from MySeqRecord import SeqRecord
from Bio import SeqIO

def __find_longer(self,seqrecord):
    if ('count' not in self.__dict__) or ('count' not in seqrecord.__dict__):
        raise IOError,"to use this function, object must have attribute 'count'"
    seqa = seqrecord.seq
    seqb = self.seq
    if seqa in seqb:
        self.count += 1
        return self
    elif seqb in seqa:
        seqrecord.count += 1
        return seqrecord
    else:
        return False

SeqRecord.find_longer = __find_longer

class Sample(object):
    def __init__(self,name):
        self.name = name
        self.single_reads = 0
        self.total_reads = 0

class NonAbundanceRecord(object):
    def __init__(self):
        self.count = 0
        
class Subject(object):
    def __init__(self,infile,out_fa,out_stat):
        self.infile = infile
        self.out_fa = out_fa
        self.out_stat = out_stat
        self.sample_set = {}
        # 
        #self.container = []
        self.container = {}

    '''O(n^2) , too slow
    def find_record(self):
        consumer = self.containerClassfy()
        consumer.next() 
        fp = open(self.infile)
        for record in SeqIO.parse(fp,'fasta'):
            record.count = 1
            sample_name = re.search('(.+)_\d+$',record.id).group(1)
            if sample_name in self.sample_set:
                record.sample = self.sample_set[sample_name]
            else:
                record.sample = Sample(sample_name)
                self.sample_set[sample_name] = record.sample
            record.sample.total_reads += 1
            consumer.send(record)
        fp.close()
   
    def containerClassfy(self):
        while True:
            record = (yield )
            for index,ct_seq in enumerate(self.container):
                find_result = ct_seq.find_longer(record)
                if find_result:
                    self.container[index] = find_result
                    break
            else:
                
    def write_stat(self):
        fp = open(self.out_stat,'w')
        total_reads = 0
        single_reads = 0
        for seq in self.container.itervalues():
            total_reads += seq.count
            if seq.count == 1:
                single_reads += 1
                seq.sample.single_reads += 1
        ratio = single_reads / total_reads * 100
        fp.write('total_reads\t%s\n'%total_reads)
        fp.write('single_reads\t%s\n'%single_reads)
        fp.write('single_ratio\t%2.2f%%\n'%ratio)
        fp.write('\nsample_name\ttotal_reads\tsingle_reads\tsingle_ratio\n')
        for sample in self.sample_set.itervalues():
            ratio = sample.single_reads / sample.total_reads * 100
            fp.write('%s\t%s\t%s\t%2.2f%%\n'%(sample.name,sample.total_reads,sample.single_reads,ratio))
        fp.close()               self.container.append(record)
    '''
    def write_fa(self):
        fp = open(self.out_fa,'w')
        for seq in self.container:
            seq.id = '%s;size=%s;'%(seq.id,seq.count)
            seq.description = ''
            fp.write(seq.format('fasta'))
        fp.close()


    def find_record(self):
        fp = open(self.infile)
        for record in SeqIO.parse(fp,'fasta'):
            record.count += 1
            sample_name = re.search('(.+)_\d+$',record.id).group(1)
            if sample_name in self.sample_set:
                record.sample = self.sample_set[sample_name]
            else:
                record.sample = Sample(sample_name)
                self.sample_set[sample_name] = record.sample
            record.sample.total_reads += 1
            if record.seq not in self.container:
                self.container[record.seq] = NonAbundanceRecord()
            self.container[record.seq].count += 1
 
    
