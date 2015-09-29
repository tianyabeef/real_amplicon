[all]
job_id = test
data_type = 16S
work_dir = /data_center_01/pipeline/16S_ITS_pipeline_v3.0/test
group_files = /data_center_01/pipeline/16S_ITS_pipeline_v3.0/test/group1.txt /data_center_01/pipeline/16S_ITS_pipeline_v3.0/test/group2.txt
group_names = group1 group2
fna_file = /data_center_01/pipeline/16S_ITS_pipeline_v3.0/test/00_data/16S_together.fna

[software]
usearch = /home/snowflake/local/bin/usearch7.0.1090_i86linux32
java = /data_center_01/soft/java/jdk-8u60/jdk1.8.0_60/bin/java
rdp_classifier = /data_center_01/home/NEOLINE/liangzebin/soft/RDPTools/classifier.jar

[scripts]
01_get_singleton_read = /data_center_01/pipeline/16S_ITS_pipeline_v3.0/script/01_get_singleton_read.py
01_rename_otu_fasta = /data_center_01/pipeline/16S_ITS_pipeline_v3.0/script/01_rename_otu_fasta.py
01_uc2otutab = /data_center_01/pipeline/16S_ITS_pipeline_v3.0/script/01_uc2otutab.py
01_otutab2fa = /data_center_01/pipeline/16S_ITS_pipeline_v3.0/script/01_otutab2fa.py
01_stat = /data_center_01/pipeline/16S_ITS_pipeline_v3.0/script/01_stat.py
01_rdp_classfier = /data_center_01/pipeline/16S_ITS_pipeline_v3.0/script/01_rdp_classfier.py

[01]
if_remain_small_size = Y
out_dir = /data_center_01/pipeline/16S_ITS_pipeline_v3.0/test/01_pick_otu
minsize = 2
strand = plus
identity = 0.97
pick_rep_set_method = most_abundant
classify_confident_cutoff = 0.8
work_dir = /data_center_01/pipeline/16S_ITS_pipeline_v3.0/test
otus_all = /data_center_01/pipeline/16S_ITS_pipeline_v3.0/test/01_pick_otu/otus_all.txt
seqs_all = /data_center_01/pipeline/16S_ITS_pipeline_v3.0/test/01_pick_otu/seqs_all.fa

[qiime]
bin_path = /data_center_01/home/liangzb/.pyenv/versions/2.7.10/bin
pick_rep_set = /data_center_01/home/liangzb/.pyenv/versions/2.7.10/bin/pick_rep_set.py
make_otu_table = /data_center_01/home/liangzb/.pyenv/versions/2.7.10/bin/make_otu_table.py
align_seqs = /data_center_01/home/liangzb/.pyenv/versions/2.7.10/bin/align_seqs.py
filter_alignment = /data_center_01/home/liangzb/.pyenv/versions/2.7.10/bin/filter_alignment.py
make_phylogeny = /data_center_01/home/liangzb/.pyenv/versions/2.7.10/bin/make_phylogeny.py
multiple_rarefactions = /data_center_01/home/liangzb/.pyenv/versions/2.7.10/bin/multiple_rarefactions.py
alpha_diversity = /data_center_01/home/liangzb/.pyenv/versions/2.7.10/bin/alpha_diversity.py
collate_alpha = /data_center_01/home/liangzb/.pyenv/versions/2.7.10/bin/collate_alpha.py

