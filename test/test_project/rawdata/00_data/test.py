import sys
sys.path.insert(1,'/data_center_01/pipeline/16S_ITS_pipeline_v3.0/bin')
from Pipeline import work_00_merge

work_00_merge('work.cfg')
