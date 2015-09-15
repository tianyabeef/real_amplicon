import sys
sys.path.insert(1,'/data_center_01/pipeline/16S_ITS_pipeline_v3.0')
import Pipeline as pp

this_script,cfg_file = sys.argv

pipeline_cfg = pp.pipeline(cfg_file)


