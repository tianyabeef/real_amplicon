echo -e 'Begin at : \c' && date
/data_center_01/pipeline/16S_ITS_pipeline_v3.0/bin/00_Merge.py /data_center_01/pipeline/16S_ITS_pipeline_v3.0/test/test_config/pre1.fq /data_center_01/pipeline/16S_ITS_pipeline_v3.0/test/test_config/pre2.fq /data_center_01/pipeline/16S_ITS_pipeline_v3.0/test/test_config/00_data -r 100000 -n name.list
 && echo This-Work-is-Completed!
echo -e 'All target finished at : \c' && date
