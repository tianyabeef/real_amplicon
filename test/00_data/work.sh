source /data_center_01/pipeline/16S_ITS_pipeline_v3.0/bin/environment.sh

echo -e 'Begin at : \c' && date
/data_center_01/pipeline/16S_ITS_pipeline_v3.0/script/00_Merge.py  /data_center_01/pipeline/16S_ITS_pipeline_v3.0/test/rawdata/pre1.fastq /data_center_01/pipeline/16S_ITS_pipeline_v3.0/test/rawdata/pre2.fastq /data_center_01/pipeline/16S_ITS_pipeline_v3.0/test/rawdata/pre3.fastq  /data_center_01/pipeline/16S_ITS_pipeline_v3.0/test/00_data -r 30000 -n /data_center_01/pipeline/16S_ITS_pipeline_v3.0/test/rawdata/name.list && echo -e 'This-Work-is-Completed! : \c' && date
echo -e 'All target finished at : \c' && date
