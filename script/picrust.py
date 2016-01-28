#!/usr/bin/env python
# -*- coding: utf-8 -*- \#
"""
@author = 'liangzb'
@date = '2016-01-22'

"""

import argparse
import sys
from util import mkdir


def read_params(args):
    parser = argparse.ArgumentParser(description='''beta anosim | v1.0 at 2015/12/23 by liangzb ''')
    parser.add_argument('-i', '--input', dest='seqs_in', metavar='FILE', type=str, required=True,
                        help="set the input seq")
    parser.add_argument('-o', '--outdir', dest='outdir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    args = parser.parse_args()
    params = vars(args)
    return params


template = '''
echo "pick_otus:enable_rev_strand_match True"  > %(outdir)s/otu_picking_params_97.txt
echo "pick_otus:similarity 0.97" >> %(outdir)s/otu_picking_params_97.txt
reference=/data_center_02/User/wucy/soft/picrust/gg_13_5_otus/rep_set/97_otus.fasta
taxanomy=/data_center_02/User/wucy/soft/picrust/gg_13_5_otus/taxonomy/97_otu_taxonomy.txt
pick_closed_reference_otus.py -i %(seqs_in)s -o %(outdir)s/ucrC97 -p %(outdir)s/otu_picking_params_97.txt -r $reference -t $taxanomy

source /data_center_02/User/wucy/soft/picrust/test_env/bin/activate
normalize_by_copy_number.py -i %(outdir)s/ucrC97/otu_table.biom -o %(outdir)s/normalized_otus.biom
predict_metagenomes.py -i %(outdir)s/normalized_otus.biom -o %(outdir)s/metagenome_predictions.biom
predict_metagenomes.py -f -i %(outdir)s/normalized_otus.biom -o %(outdir)s/metagenome_predictions.tab
predict_metagenomes.py --type_of_prediction cog -i %(outdir)s/normalized_otus.biom -o %(outdir)s/metagenome_predictions.cog.biom
predict_metagenomes.py -f --type_of_prediction cog -i %(outdir)s/normalized_otus.biom -o %(outdir)s/metagenome_predictions.cog.tab

categorize_by_function.py -i %(outdir)s/metagenome_predictions.biom -c KEGG_Pathways -l 3 -o %(outdir)s/metagenome_predictions.L3.biom
categorize_by_function.py -f -i %(outdir)s/metagenome_predictions.biom -c KEGG_Pathways -l 3 -o %(outdir)s/metagenome_predictions.L3.txt
categorize_by_function.py -i %(outdir)s/metagenome_predictions.biom -c KEGG_Pathways -l 2 -o %(outdir)s/metagenome_predictions.L3.biom
categorize_by_function.py -f -i %(outdir)s/metagenome_predictions.biom -c KEGG_Pathways -l 2 -o %(outdir)s/metagenome_predictions.L2.txt

echo "summarize_taxa:md_identifier\tKEGG_Pathways" > %(outdir)s/qiime_params.txt
echo "summarize_taxa:absolute_abundance\tTrue" >> %(outdir)s/qiime_params.txt
echo "summarize_taxa:level\t2" >> %(outdir)s/qiime_params.txt
summarize_taxa_through_plots.py -i %(outdir)s/metagenome_predictions.L2.txt -p %(outdir)s/qiime_params.txt -o %(outdir)s/plots_at_level2

metagenome_contributions.py -i %(outdir)s/normalized_otus.biom -l K00001,K00002,K00004 -o %(outdir)s/ko_metagenome_contributions.tab
metagenome_contributions.py -i %(outdir)s/normalized_otus.biom -l COG0001,COG0002 -t cog -o %(outdir)s/cog_metagenome_contributions.tab

deactivate
'''

if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['outdir'])
    commands = template % params
    with open('%s/commands.sh' % params['outdir'], 'w') as out:
        out.write(commands)
