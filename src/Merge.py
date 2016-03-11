from __future__ import division
import random
import re
import os
import sys
import gzip
import numpy as np
from Bio import SeqIO
from MySeqRecord import SeqRecord


class Sample(object):
    def __init__(self, sample_name, required_data):
        self.name = sample_name
        self.needed_data = self._get_need_data(required_data)
        self.stats = {}
        self.stats['tags'] = 0
        self.stats['bases'] = 0
        self.stats['Q20'] = 0
        self.stats['Q30'] = 0
        self.stats['GC'] = 0
        self.stats['length'] = []

    def init_handle(self, outdir):
        if not os.path.isdir(outdir):
            os.mkdir(outdir)
        outfile = '%s/%s.fq.gz' % (outdir, self.name)
        self.out = gzip.open(outfile, 'wb')

    def release_handle(self):
        self.out.close()

    def _get_need_data(self, n):
        n = int(n)
        r = random.uniform(-0.1, 0.1)
        return int(n * (1.2 + r))


class Subject(object):
    def __init__(self, infile_list, upload_dir,
                 out_fasta_file, out_stat_file,
                 required_data, out_length_file,
                 max_length, min_length, length_step,
                 upload_stat=None,
                 name_table_file=None):
        self.infile_list = infile_list
        self.required_data = required_data
        self.out_fasta_file = out_fasta_file
        self.out_length_file = out_length_file
        self.max_length = max_length
        self.min_length = min_length
        self.length_step = length_step
        self.stat_file = out_stat_file
        self.upload_stat_file = upload_stat
        self.upload_dir = upload_dir
        self.name_table_file = name_table_file
        self.sample_set = {}
        self.name_table = {}
        self.length = {}

    def read_name_table(self):
        try:
            name_table = open(self.name_table_file)
        except IOError, ex:
            sys.stderr.write('There is no file to open!')
            return False
        for line in name_table:
            #            tabs = re.split('\s+',line.strip())
            tabs = line.strip().split('\t')
            self.name_table[tabs[0]] = tabs[1]
        name_table.close()
        return True

    def init_sample(self, sample_name):
        if self.name_table:
            try:
                sample_name = self.name_table[sample_name]
            except KeyError, ex:
                return None
        if sample_name not in self.sample_set:
            sample_obj = Sample(sample_name, self.required_data)
            sample_obj.init_handle(self.upload_dir)
            self.sample_set[sample_name] = sample_obj
        sample_obj = self.sample_set[sample_name]
        return sample_obj

    def output(self, record, sample):
        out_record = SeqRecord(seq=record.seq,
                               id='%s_%s' % (sample.name, sample.stats['tags']),
                               description='')
        self.out_fasta.write(out_record.format('fasta'))
        record.description = ''
        sample.out.write(record.format('fastq'))

    def merge_with_infile(self, infile):
        for record in SeqIO.parse(open(infile), 'fastq'):
            description = record.description
            try:
                sample = re.search('(\S+)_\d+$', description).group(1)
            except AttributeError:
                sys.stderr.write('sample name maybe some error, use read description as sample_name')
                sample = description
            sample = self.init_sample(sample)
            if sample is None:
                continue
            if sample.stats['tags'] >= sample.needed_data:
                continue
            length = len(record)
            sample.stats['tags'] += 1
            sample.stats['bases'] += length
            q20, q30 = record.Q20_Q30()
            sample.stats['Q20'] += q20
            sample.stats['Q30'] += q30
            sample.stats['GC'] += record.GC()
            sample.stats['length'].append(length)
            if length not in self.length:
                self.length[length] = 0
            self.length[length] += 1
            self.output(record, sample)

    def merge(self):
        self.out_fasta = open(self.out_fasta_file, 'w')
        for infile in self.infile_list:
            self.merge_with_infile(infile)
        for sample in self.sample_set.itervalues():
            sample.release_handle()
        self.out_fasta.close()

    def write_stat(self):
        out_stat = open(self.stat_file, 'w')
        out_stat.write('Sample_name\tTags\tBases\tQ20\tQ30\n')
        for sample in self.sample_set.itervalues():
            out_stat.write('%s\t%s\t%s\t%s\t%s\n' % (sample.name,
                                                     sample.stats['tags'],
                                                     sample.stats['bases'],
                                                     sample.stats['Q20'],
                                                     sample.stats['Q30']))
        out_stat.close()

    def upload_stat(self):
        stat_file = open(self.upload_stat_file, 'w')
        stat_file.write('Sample name\tClean Reads\tBases(bp)\tQ20(%)\tQ30(%)\tGC(%)\tAverage length(bp)\n')
        for sample in self.sample_set.itervalues():
            Q20_percent = sample.stats['Q20'] / sample.stats['bases'] * 100
            Q30_percent = sample.stats['Q30'] / sample.stats['bases'] * 100
            GC_percent = sample.stats['GC'] / sample.stats['bases'] * 100
            average_length = int(np.mean(sample.stats['length']))  #输出整数
            stat_file.write('%s\t%s\t%s\t%2.2f%%\t%2.2f%%\t%2.2f%%\t%s\n' % (sample.name,
                                                                             sample.stats['tags'],
                                                                             sample.stats['bases'],
                                                                             Q20_percent,
                                                                             Q30_percent,
                                                                             GC_percent,
                                                                             average_length))

    def write_length(self):
        out_length = open(self.out_length_file, 'w')
        out_length.write('length\tnum\n')
        r = range(self.min_length, self.max_length + self.length_step, self.length_step)
        for index in range(len(r) - 1):
            b = r[index]
            e = r[index + 1]
            length = 0
            for l in range(b, e):
                try:
                    length += self.length[l]
                except KeyError, ex:
                    continue
            length_range = '%s-%s' % (b, e)
            out_length.write('%s\t%s\n' % (length_range, length))
        out_length.close()
