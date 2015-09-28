from qiime.rarefaction import RarefactionMaker

class MyRarefactionMaker(RarefactionMaker):

    def __init__(self, otu_path, range, num_reps):
        """ init a rarefactionmaker

        otu_path is path to .biom otu table
        we just ignore any rarefaction levels beyond any sample in the data
        """
        self.rare_depths = range
        self.num_reps = num_reps
        self.otu_table = self.getBiomData(otu_path)
        self.max_num_taxa = -1
        tmp = -1
        for val in self.otu_table.iter_data(axis='observation'):
            if val.sum() > tmp:
                tmp = val.sum()
        self.max_num_taxa = tmp

