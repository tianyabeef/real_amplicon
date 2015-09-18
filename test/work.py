import sys
sys.path.insert(1,'/data_center_01/pipeline/16S_ITS_pipeline_v3.0')

from Pipeline import work_00_merge
from Pipeline import work_01_pick_otu,work_01_alpha_rare

cfg = work_00_merge('work.cfg')
cfg = work_01_pick_otu(cfg)
cfg = work_01_alpha_rare(cfg)
