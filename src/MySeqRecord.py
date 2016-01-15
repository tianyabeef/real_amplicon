import numpy as np
from Bio.SeqRecord import SeqRecord


def __N_count(self):
    return self.seq.count('N')


def __Q_ave(self):
    qlist = list(self.letter_annotations.itervalues())[0]
    Q_ave = np.mean(filter(lambda s: s > 30, qlist))
    if Q_ave is np.nan:
        return None
    else:
        return Q_ave


def __high_quality_count(self):
    q20_count = 0
    q30_count = 0
    qlist = list(self.letter_annotations.itervalues())[0]
    for q in qlist:
        if q >= 20:
            q20_count += 1
        if q >= 30:
            q30_count += 1
    return q20_count, q30_count


def __GC(self):
    return self.seq.count('G') + self.seq.count('C')


SeqRecord.Q_ave = __Q_ave
SeqRecord.N_count = __N_count
SeqRecord.Q20_Q30 = __high_quality_count
SeqRecord.GC = __GC
