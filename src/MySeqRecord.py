from Bio.SeqRecord import SeqRecord

def __N_count(self):
    N_count = 0;
    for char in self.seq:
        if char == 'N':
            N_count += 1
    return N_count
def __Q_ave(self):
    Q_sum = 0
    qlist = list(self.letter_annotations.itervalues())[0]
    for q in qlist:
        Q_sum += q
    Q_ave = Q_sum / len(self)
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
    return q20_count,q30_count


SeqRecord.Q_ave = __Q_ave
SeqRecord.N_count = __N_count
SeqRecord.Q20_Q30 = __high_quality_count

