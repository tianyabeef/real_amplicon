import sys

class ReadsStat(object):
    def __init__(self, sampleName, clean_read, base, q20, q30, gc, average_length):
        self.sampleName = sampleName
        self.clean_read = clean_read
        self.base = base
        self.q20 = q20
        self.q30 = q30
        self.gc = gc
        self.average_length = average_length


class ReadsLength(object):
    def __init__(self, name, num):
        self.name = name
        self.num = num


class OtuStatistical(object):
    '''
    classdocs
    '''

    def __init__(self, sampleName, amplicon_type, clean_read, q20, q30,
                 singleton, singleton_ratio, mapped_reads, mapped_ratio, otus):
        self.sampleName = sampleName
        self.amplicon_type = amplicon_type
        self.clean_read = clean_read
        self.q20 = q20
        self.q30 = q30
        self.singleton = singleton
        self.singleton_ratio = singleton_ratio
        self.mapped_reads = mapped_reads
        self.mapped_ratio = mapped_ratio
        self.otus = otus

    def __init__(self, sampleName, amplicon_type, clean_read, mapped_reads, mapped_ratio, otus):
        self.sampleName = sampleName
        self.amplicon_type = amplicon_type
        self.clean_read = clean_read
        self.mapped_reads = mapped_reads
        self.mapped_ratio = mapped_ratio
        self.otus = otus


class OtuStatisticalDownsize(object):
    def __init__(self, sample_name, downsize, otus_before, otus_after):
        self.sample_name = sample_name
        self.downsize = downsize
        self.otus_before = otus_before
        self.otus_after = otus_after


class CoreMicrobiome(object):
    def __init__(self, otu_id, taxonomy_level, taxonomy_name):
        self.otu_id = otu_id
        self.taxonomy_level = taxonomy_level
        self.taxonomy_name = taxonomy_name


class OtuAssignmentsStatistical(object):
    def __init__(self, assignmentsName, num):
        self.assignmentsName = assignmentsName
        self.num = num


class Alpha_diversity(object):
    def __init__(self, alphaName, chao1, goods_coverage, observed_species,
                 whole_tree, shannon, simpson):
        self.alphaName = alphaName
        self.chao1 = chao1
        self.goods_coverage = goods_coverage
        self.observed_species = observed_species
        self.whole_tree = whole_tree
        self.shannon = shannon
        self.simpson = simpson
class Obj(object):
    pass
def createClass(file):
    obj_list = []
    try:
        with open(file) as fq:
            list = fq.next().strip().split("\t")
            list.insert(0, "sampleName")
            for line in fq:
                obj = Obj()
                array = line.strip().split("\t")
                if len(list) == len(array):
                    for i in range(0,len(list)):
                        obj.__setattr__(list[i],array[i])
                    obj_list.append(obj)
                else:
                    del list[0]
                    for i in range(0,len(list)):
                        obj.__setattr__(list[i],array[i])
                    obj_list.append(obj)                
    except IOError:
        sys.stderr.write('%s file not found!\n' % file)
    return obj_list        
