from __future__ import division
import random
import re
import os
import sys
import gzip
from Bio import SeqIO
from MySeqRecord import SeqRecord

class Sample(object):
    def __init__(self,sample_name,required_data):
        self.name = sample_name
        self.needed_data = self._get_need_data(required_data)
        self.stats = {}
        self.stats['tags'] = 0
        self.stats['bases'] = 0
        self.stats['Q20'] = 0
        self.stats['Q30'] = 0

    def init_handle(self,outdir):
        if not os.path.isdir(outdir):
            os.mkdir(outdir)
        outfile = '%s/%s.fq.gz'%(outdir,self.name)
        self.out = gzip.open(outfile,'wb')

    def release_handle(self):
        self.out.close()
        
    def _get_need_data(self,n):
        n = int(n)
        r = random.uniform(-0.1,0.1)
        return int( n * (1.2 + r) )

class Subject(object):
    def __init__(self,infile_list,out_dir,required_data,name_table_file=None):
        self.infile_list = infile_list
        self.required_data = required_data
        self.out_fasta_file = '%s/16S_together.fna'%out_dir
        self.stat_file = '%s/16S_together.stat'%out_dir
        self.out_dir = out_dir
        self.name_table_file = name_table_file
        self.sample_set = {}
        self.name_table = {}

    def read_name_table(self):
        try:
            name_table = open(self.name_table_file)
        except IOError,ex:
            sys.stderr.write('There is no file to open!')
            return False
        for line in name_table:
            tabs = re.split('\s+',line.strip())
            self.name_table[tabs[0]] = tabs[1]
        name_table.close()
        return True

    def init_sample(self,sample_name):
        if self.name_table:
            sample_name = self.name_table[sample_name]
        if sample_name not in self.sample_set:
            sample_obj = Sample(sample_name,self.required_data)
            sample_obj.init_handle('%s/upload'%self.out_dir)
            self.sample_set[sample_name] = sample_obj
        sample_obj = self.sample_set[sample_name]
        return sample_obj

    def output(self,record,sample):
        out_record = SeqRecord(seq=record.seq,id='%s_%s'%(sample.name,sample.stats['tags']),description='')
        self.out_fasta.write(out_record.format('fasta'))
        record.description = ''
        sample.out.write(record.format('fastq'))

    def merge_with_infile(self,infile):
        for record in SeqIO.parse(open(infile),'fastq'):
            description = record.description
            sample = re.search('(\S+)_\d+',description).group(1)
            sample = self.init_sample(sample)
            if sample.stats['tags'] >= sample.needed_data:
                continue
            sample.stats['tags'] += 1
            sample.stats['bases'] += len(record)
            q20,q30 = record.Q20_Q30()
            sample.stats['Q20'] += q20
            sample.stats['Q30'] += q30
            self.output(record,sample)

    def merge(self):
        self.out_fasta = open(self.out_fasta_file,'w')
        for infile in self.infile_list:
            self.merge_with_infile(infile)
        for sample in self.sample_set.itervalues():
            sample.release_handle()
        self.out_fasta.close()

    def write_stat(self):
        out_stat = open(self.stat_file,'w')
        out_stat.write('Sample_name\tTags\tBases\tQ20\tQ30\n')
        for sample in self.sample_set.itervalues():
            out_stat.write('%s\t%s\t%s\t%s\t%s\n'%(sample.name,sample.stats['tags'],sample.stats['bases'],sample.stats['Q20'],sample.stats['Q30']))
        out_stat.close()

