#!/usr/bin/env python
# -*- coding: utf-8 -*- #
'''
Created on Oct 22, 2015

@author: root
'''
import ConfigParser
import sys
import argparse
import re
from jinja2 import Environment,FileSystemLoader
import operator
class OtuStatistical(object):
    '''
    classdocs
    '''
    def __init__(self, sampleName, amplicon_type, clean_read, q20, q30, singleton,singleton_ratio, mapped_reads,mapped_ratio,otus):
        self.sampleName=sampleName
        self.amplicon_type=amplicon_type
        self.clean_read=clean_read
        self.q20=q20
        self.q30=q30
        self.singleton=singleton
        self.singleton_ratio=singleton_ratio
        self.mapped_reads=mapped_reads
        self.mapped_ratio = mapped_ratio
        self.otus=otus
class OtuStatisticalDownsize(object):
    def __init__(self,sample_name,downsize,otus_before,otus_after):
        self.sample_name = sample_name
        self.downsize=downsize
        self.otus_before = otus_before
        self.otus_after = otus_after
class CoreMicrobiome(object):
    def __init__(self,otu_id, taxonomy_level,taxonomy_name):
        self.otu_id=otu_id
        self.taxonomy_levle=taxonomy_level
        self.taxonomh_name=taxonomy_name
class OtuAssignmentsStatistical(object):
    def __init__(self,assignmentsName,num):
        self.assignmentsName=assignmentsName
        self.num=num
class Alpha_diversity(object):
    def __init__(self,alphaName,chao1, goods_coverage, observed_species, whole_tree, shannon, simpon):
        self.alphaName=alphaName
        self.chao1 =chao1
        self.goods_coverage=goods_coverage
        self.observed_species=observed_species
        self.whole_tree=whole_tree
        self.shannon=shannon
        self.simpon=simpon
# class Beta_diversity_weighted(object):
#     def __init__(self,name):
#         self.name=name

def save_table(input_dir):
#save table
    weight_unifrac_data_list=[]
    weight_unifrac_jqGrid_list=[]
    sampleName="'"
    with open(input_dir) as lines:
        head = lines.next()
        samples_name = head.strip().split('\t')[1:]
        for line in lines:
            str='{'
            jqGrid = ''
            tabs = line.strip().split("\t")
            str+='name:'+tabs[0]+','
            for i,value in enumerate(samples_name):
                if len(sample_name)<9:
                    
                    if i<len(samples_name)-1:
                        sampleName += value+"','"
                        str += value+":"+tabs[i+1]
                        str += ","
                        jqGrid += "name:"+value+",index:"+value+",aligen:center,width:90},"
                    else:
                        sampleName += value+"','"
                        jqGrid += "name:"+value+",index:"+value+",aligen:center,width:90}"
                        str += value+":"+tabs[i+1]
                        str +='}'
                else:
                    
                    if i<8:
                        sampleName += value+"','"
                        str += value+":"+tabs[i+1]
                        str += ","
                        jqGrid += "name:"+value+",index:"+value+",aligen:center,width:90},"
                    else:
                        sampleName += value+"'"
                        jqGrid += "name:"+value+",index:"+value+",aligen:center,width:90}"
                        str += value+":"+tabs[i+1]
                        str +='}'
                        break
        weight_unifrac_data_list.append(str)
        weight_unifrac_jqGrid_list.append(jqGrid)
    return [weight_unifrac_data_list,weight_unifrac_jqGrid_list,sampleName]
def read_params(args):
    parser = argparse.ArgumentParser(description='get_html ')
    parser.add_argument('-c','--config',dest='config',metavar='FILE',type=str,required=True,
                        help="set the input file")
    args = parser.parse_args()
    params = vars(args)
    return params

def get_html():
    params = read_params(sys.argv)
    config = ConfigParser.ConfigParser()
    config.read(params['config'])
    reload(sys)
    sys.setdefaultencoding('utf-8')
    out_dir_report=work_dir+'/'+'report/'
    work_dir = config.get('params','work_dir')
    data_type = config.get('params','data_type')
    group_files = re.split('\s+',config.get('params','group_files'))
    group_file_origin =group_files[0]
    group_file = re.search('.+\/(.+)\..+', group_file_origin).group(1)
    
#save table
    var_html = {}
    tabs=[]
    otuStatisticals={}
    with open(work_dir+"../"+config.get('origin','pick_otu_txt'),'r') as lines:
        var_html['sample_sum']=int(lines.next().strip().split(":")[1])
        var_html['otu_sum'] = int(lines.next().strip().split(":")[1])
        lines.next()
        lines.next()
        lines.next()
        lines.next()
        for line in lines:
            tabs = line.strip().split("\t")
            #sample_name amplicon_type tags mapped_reads mapped_ratio
            otuStatistical=OtuStatistical(tabs[0],data_type,tabs[1],tabs[8],tabs[9],tabs[4],tabs[5],tabs[2],tabs[3],tabs[10])
            otuStatisticals[tabs[0]] = otuStatistical
            
#save table
    otuStatisticalDownsizes={}
    with open(work_dir+"../"+config.get('origin','otu_all_downsize_txt'),'r') as lines:
        lines.next()
        for line in lines:
            tabs = line.strip().split('\t')
            otuStatisticalDownsize=OtuStatisticalDownsize(tabs[0],tabs[1],tabs[2],tabs[3])
            otuStatisticalDownsizes[tabs[0]] = otuStatisticalDownsize

#save tabel CoreMicrobiome
    coreMicrobiomes={}
    with open(work_dir+"../"+config.get('origin','group_core_otu_txt').replace("#group",group_file),'r') as lines:
        lines.next()
        for line in lines:
            tabs = line.strip().split("\t")
            coreMicrobiome = CoreMicrobiome(tabs[0],tabs[1],tabs[2])
            coreMicrobiomes[tabs[0]] = coreMicrobiome

#save table
    otuAssignmentsStatisticals={}
    with open(work_dir+"../"+config.get('origin','otu_statistic_txt'),'r') as lines:
        lines.next()
        for line in lines:
            tabs = line.strip().split('\t')
            otuAssignmentsStatistical=OtuAssignmentsStatistical(tabs[0],tabs[1])
            otuAssignmentsStatisticals[tabs[0]]=otuAssignmentsStatistical

#save table
    alpha_diversitys={}
    with open(work_dir+"../"+config.get('origin','group_alpha_statistic_txt').replace("#group",group_file),'r') as lines:
        lines.next()
        for line in lines:
            tabs = line.strip().split('\t')
            alpha_diversity=Alpha_diversity(tabs[0],tabs[1],tabs[2],tabs[3],tabs[4],tabs[5],tabs[6])
            alpha_diversitys[tabs[0]]=alpha_diversity

#save table
    alpha_diversity_diffs={}
    with open(work_dir+"../"+config.get('origin','group_alpha_makers_txt').replace("#group",group_file),'r') as lines:
        lines.next()
        for line in lines:
            tabs = line.strip().split('\t')
            alpha_diversity=Alpha_diversity(tabs[0],tabs[1],tabs[2],tabs[3],tabs[4],tabs[5],tabs[6])
            alpha_diversity_diffs[tabs[0]]=alpha_diversity

#save_table
    beta_un_diversity= save_table(work_dir+"../"+config.get('origin','group_beta_div_un_txt').replace("#group",group_file))
#save_table
    beta_diversity= save_table(work_dir+"../"+config.get('origin','group_beta_div_txt').replace("#group",group_file))
#save_table
    diff_otu_marker= save_table(work_dir+"../"+config.get('origin','group_diff_otu_marker_txt').replace("#group",group_file))
#save_table
    diff_genus_marker= save_table(work_dir+"../"+config.get('origin','group_diff_genus_marker_txt').replace("#group",group_file))
#save_table
    diff_taxall_marker= save_table(work_dir+"../"+config.get('origin','group_diff_taxall_marker_txt').replace("#group",group_file))
#save_table
    diff_phylum_marker= save_table(work_dir+"../"+config.get('origin','group_diff_phylum_marker_txt').replace("#group",group_file))
#save_table
    env = Environment(loader=FileSystemLoader(out_dir_report+'js/',encoding='utf-8'))
    template = env.get_template('table_template.js')
    otuStatisticals = sorted(otuStatisticals.iteritems(),key=operator.itemgetter(1),reverse=True)
    table = template.render(otuStatisticals=otuStatisticals,otuStatisticalDownsizes=otuStatisticalDownsizes,
                            otuAssignmentsStatisticals =otuAssignmentsStatisticals,alpha_diversitys=alpha_diversitys,
                            alpha_diversity_diffs = alpha_diversity_diffs,beta_diversity_data=beta_diversity[0],beta_diversity_jqGrid=beta_diversity[1],
                            beta_diversity_sampeName=beta_diversity[2],beta_un_diversity_data=beta_un_diversity[0],beta_un_diversity_jqGrid=beta_un_diversity[1],
                            beta_un_diversity_sampeName=beta_un_diversity[2],coreMicrobiomes=coreMicrobiomes,
                            diff_otu_marker_data=diff_otu_marker[0],diff_otu_marker_jqGrid=diff_otu_marker[1],diff_otu_marker_sampleName=diff_otu_marker[2],
                            diff_genus_marker_data = diff_genus_marker[0],diff_genus_marker_jqGrid = diff_genus_marker[1],diff_genus_marker_sampleName = diff_genus_marker[3],
                            diff_taxall_marker_data = diff_taxall_marker[0], diff_taxall_marker_jqGrid = diff_taxall_marker[1],diff_taxall_marker_sampleName= diff_taxall_marker[3],
                            diff_phylum_marker_data = diff_phylum_marker[0],diff_phylum_marker_jqGrid = diff_phylum_marker[1],diff_phylum_marker_sampleName = diff_phylum_marker[3])
    with open(work_dir+'report/js/table.js','w') as fp:
        fp.write(table)
    #finally_get_html

#    sample_num_in_groups,min_sample_mun_in_groups,sample_num_total,group_num = parse_group(group_file_origin)
    var_html['amplification']=data_type
    var_html['core_microbiome']=len(coreMicrobiomes)
    var_html['star_picture_top']=10
    var_html['Phylogenetic_genus_top']=10
    var_html['diff_otus']=len(diff_otu_marker[0])
    var_html['diff_genus']=len(diff_genus_marker[0])
    var_html['diff_species']=len(diff_taxall_marker[0])
    var_html['diff_phylum']=len(diff_phylum_marker[0])
    var_html['group_num']=len(group_files)
    var_html['p_value']=0.05
    
    var_html['reads_statistical']=True
    var_html['otu_statistical']=True
    var_html['downsize_html']=True
    
    var_html['core_microbiome_html']=True
    var_html['otu_venn']=True
    var_html['otu_pca']=True
    
    var_html['specaccum']=True
    
    var_html['otu_tax_assignments']=True
    var_html['otu_annotation_statistical']=True
    var_html['tax_summary']=True
    var_html['otu_heatmap']=True
    var_html['otu_krona']=True
    var_html['phylogenetic_tree']=True
    var_html['alpha_diversity']=True
    var_html['alpha_diff']=True
    var_html['uniFra_analysis']=True
    var_html['similarity_analysis']=True
    var_html['lefse']=True
    var_html['diff_analysis']=False
    
    env = Environment(loader=FileSystemLoader(out_dir_report+'/templates',encoding='utf-8'))
    template = env.get_template('report.html')
    finally_html = template.render(var_html)
    with open(work_dir+'report/index_loaded.html','w') as fp:
        fp.write(finally_html)
    templetaPDF = env.get_template('pdf.html')
    pdf = templetaPDF.render(var_html)
    with open(work_dir+'report/pdf.html','w') ad fp:
        fp.write(pdf)
if __name__ == '__main__':
    get_html()


