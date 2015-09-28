import sys
sys.path.insert(1,'/data_center_01/pipeline/16S_ITS_pipeline_v3.0')

from Pipeline import work_00_merge
from Pipeline import work_01_pick_otu,work_01_alpha_rare
from Pipeline import work_02_otu_table

cfg,sh0 = work_00_merge('work.cfg')
cfg,sh1 = work_01_pick_otu(cfg)
cfg,sh1_rare = work_01_alpha_rare(cfg)
cfg.sh2 = work_02_otu_table(cfg)
