'''
Created on Oct 22, 2015

@author: root
'''
import ConfigParser
import sys
import os
import argparse
import re
from jinja2 import Environment,FileSystemLoader
import operator
class OtuStatistical(object):
    '''
    classdocs
    '''
    def __init__(self, name, amplicon_type, clean_read, q20, q30, singleton,singleton_ratio, mapped_reads,mapped_ratio,otus):
        self.name=name
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
    def __init__(self,name,num):
        self.name=name
        self.num=num
class Alpha_diversity(object):
    def __init__(self,name,chao1, goods_coverage, observed_species, whole_tree, shannon, simpon):
        self.name=name
        self.chao1 =chao1
        self.goods_coverage=goods_coverage
        self.observed_species=observed_species
        self.whole_tree=whole_tree
        self.shannon=shannon
        self.simpon=simpon
class Beta_diversity_weighted(object):
    def __init__(self,name):
        self.name=name

def save_table(input_dir):
#save table

    
    weight_unifrac_data_list=[]
    weight_unifrac_jqGrid_list=[]
    with open(input_dir) as lines:
        head = lines.next()
        samples_name = head.strip().split('\t')[1:]
        for line in lines:
            str='{'
            jqGrid = ''
            tabs = line.strip().split("\t")
            str+='name:'+tabs[0]+','
            for i,sample_name in enumerate(samples_name):
                if len(sample_name)<9:
                    if i<len(samples_name)-1:
                        str += sample_name+":"+tabs[i+1]
                        str += ","
                        jqGrid += "name:"+sample_name+",index:"+sample_name+",aligen:center,width:90},"
                    else:
                        jqGrid += "name:"+sample_name+",index:"+sample_name+",aligen:center,width:90}"
                        str += sample_name+":"+tabs[i+1]
                        str +='}'
                else:
                    if i<8:
                        str += sample_name+":"+tabs[i+1]
                        str += ","
                        jqGrid += "name:"+sample_name+",index:"+sample_name+",aligen:center,width:90},"
                    else:
                        jqGrid += "name:"+sample_name+",index:"+sample_name+",aligen:center,width:90}"
                        str += sample_name+":"+tabs[i+1]
                        str +='}'
                        break
    weight_unifrac_data_list.append(str)   
    weight_unifrac_jqGrid_list.append(jqGrid)         
    return [weight_unifrac_data_list,weight_unifrac_jqGrid_list]
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
    work_dir = config.get('params','work_dir')
    group_files = config.get('params','group_files')
    html_template = config.get('params','html_template')
    data_type = config.get('params','data_type')
    group_num = config.get('params','group_num')
    out_dir_report=work_dir+'/'+'report/'
    image_dir = out_dir_report+'/image/'
    origin = config.items('origin')
    
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
            otuStatisticals[tabs[0]]=otuStatistical
        
#save table
    otuStatisticalDownsizes={}
    with open(work_dir+"../"+config.get('origin','otu_all_downsize_txt'),'r') as lines:
        lines.next()
        for line in lines:
            tabs = line.strip().split('\t')
            otuStatisticalDownsize=OtuStatisticalDownsize(tabs[0],tabs[1],tabs[2],tabs[3])
            otuStatisticalDownsizes[tabs[0]] =    otuStatisticalDownsize


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
    print work_dir+"../"+config.get('origin','group_beta_div_un_txt').replace("#group",group_file)
    beta  = save_table(work_dir+"../"+config.get('origin','group_beta_div_un_txt').replace("#group",group_file))
    
#save_table
    env = Environment(loader=FileSystemLoader(html_template+'js/',encoding='utf-8'))
    template = env.get_template('table_template.js')
    sorted(otuStatisticals.iteritems(),key=operator.itemgetter(1),reverse=True)
    table = template.render(otuStatisticals=otuStatisticals,otuStatisticalDownsizes=otuStatisticalDownsizes,
                            otuAssignmentsStatisticals =otuAssignmentsStatisticals,alpha_diversitys=alpha_diversitys,
                            alpha_diversity_diffs = alpha_diversity_diffs,beta_data=beta[0],beta_jqGrid=beta[1],
                            )
    with open(work_dir+'report/js/table.js','w') as fp:
        fp.write(table)
    #finally_get_html

#    sample_num_in_groups,min_sample_mun_in_groups,sample_num_total,group_num = parse_group(group_file_origin)
    var_html['amplification']=data_type
    var_html['core_microbiome']=10
    var_html['star_picture_top']=10
    var_html['Phylogenetic_genus_top']=10
    var_html['diff_otus']=10
    var_html['diff_genus']=10
    var_html['diff_species']=10
    var_html['group_num']=10
    var_html['p_value']=0.05
    var_html['reads_statistical']=True
    var_html['otu_statistical']=True
    var_html['downsize_html']=True
    var_html['core_microbiome_html']=True
    var_html['otu_venn=True']=True
    env = Environment(loader=FileSystemLoader(out_dir_report+'/templates',encoding='utf-8'))
    template = env.get_template('1.1reads_statistical.html')
    finally_html = template.render(var_html)
    with open(work_dir+'report/index_loaded.html','w') as fp:
        fp.write(finally_html)

if __name__ == '__main__':
    get_html()
