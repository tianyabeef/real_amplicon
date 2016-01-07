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
from jinja2 import Environment, FileSystemLoader
import operator
import os

this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../bin')
from settings import *


class OtuStatistical(object):
    '''
    classdocs
    '''

    def __init__(self, sampleName, amplicon_type, clean_read, q20, q30,
                 singleton, singleton_ratio, mapped_reads, mapped_ratio, otus):
        self.sampleName = sampleName
        self.amplicon_type = amplicon_type
        self.clean_read = clean_read
        self.q20 = q20
        self.q30 = q30
        self.singleton = singleton
        self.singleton_ratio = singleton_ratio
        self.mapped_reads = mapped_reads
        self.mapped_ratio = mapped_ratio
        self.otus = otus


class OtuStatisticalDownsize(object):
    def __init__(self, sample_name, downsize, otus_before, otus_after):
        self.sample_name = sample_name
        self.downsize = downsize
        self.otus_before = otus_before
        self.otus_after = otus_after


class CoreMicrobiome(object):
    def __init__(self, otu_id, taxonomy_level, taxonomy_name):
        self.otu_id = otu_id
        self.taxonomy_level = taxonomy_level
        self.taxonomy_name = taxonomy_name


class OtuAssignmentsStatistical(object):
    def __init__(self, assignmentsName, num):
        self.assignmentsName = assignmentsName
        self.num = num


class Alpha_diversity(object):
    def __init__(self, alphaName, chao1, goods_coverage, observed_species,
                 whole_tree, shannon, simpson):
        self.alphaName = alphaName
        self.chao1 = chao1
        self.goods_coverage = goods_coverage
        self.observed_species = observed_species
        self.whole_tree = whole_tree
        self.shannon = shannon
        self.simpson = simpson


def stringasfloat(string):
    try:
        num = float(string)
    except ValueError:
        return string
        #  print string
    if (num >= 0.01):
        value = format(num, '.2f')
    else:
        value = format(num, '.2e')
    if num == 0:
        value = 0
    return value


def html_translate(str):
    str = str.replace('"', '&quot;')
    str = str.replace('&', '&amp;')
    str = str.replace('<', '&lt;')
    str = str.replace('>', '&gt;')
    return str


def save_table(input_dir):
    # save tablei
    exist = True
    weight_unifrac_data_list = []
    weight_unifrac_jqGrid_list = []
    sampleName = "'"
    try:
        with open(input_dir) as lines:
            head = lines.next()
            head = html_translate(head)
            samples_name = head.strip().split('\t')
            samples_name.insert(0, "sampleName")
            if (len(samples_name) > 10):
                samples_name_two = samples_name[:10]
                sampleName = ("','").join(samples_name_two)
            else:
                sampleName = ("','").join(samples_name)
            jqGrid_head = "{name:'sampleName',index:'sampleName',width:140,align:'center'},"
            weight_unifrac_jqGrid_list.append(jqGrid_head)
            count = 0
            samples_name = samples_name[1:]
            for_time = []
            for i, value in enumerate(samples_name):
                for_time.append("%s%d" % ("sample", i))
            for line in lines:
                line = html_translate(line)
                count += 1
                tabs = line.strip().split("\t")
                str = "{sampleName:\"" + tabs[0] + "\","
                for i, value in enumerate(for_time):
                    jqGrid = '{'
                    if len(for_time) < 9:

                        if i < len(for_time) - 1:
                            str += '%s:"%s",' % (
                                value, stringasfloat(tabs[i + 1]))
                            # str += value+":\""+tabs[i+1]+"\","
                            jqGrid += "name:'" + value + "',index:'" + value + "',align:'center',width:90},"
                        else:
                            jqGrid += "name:'" + value + "',index:'" + value + "',align:'center',width:90}"
                            str += '%s:"%s"' % (
                                value, stringasfloat(tabs[i + 1]))
                            # str += value+":\""+tabs[i+1]+"\""
                            str += '},'
                        if count == 1:
                            weight_unifrac_jqGrid_list.append(jqGrid)
                    else:

                        if i < 8:
                            str += '%s:"%s",' % (
                                value, stringasfloat(tabs[i + 1]))
                            # str += value+":\""+tabs[i+1]+"\","
                            jqGrid += "name:'" + value + "',index:'" + value + "',align:'center',width:90},"
                            if count == 1:
                                weight_unifrac_jqGrid_list.append(jqGrid)
                        else:
                            jqGrid += "name:'" + value + "',index:'" + value + "',align:'center',width:90}"
                            str += '%s:"%s"' % (
                                value, stringasfloat(tabs[i + 1]))
                            # str += value+":\""+tabs[i+1]+"\""
                            str += '},'
                            if count == 1:
                                weight_unifrac_jqGrid_list.append(jqGrid)
                            break
                weight_unifrac_data_list.append(str)
            if count == 0:
                return [[], [], None, False]
    except IOError:
        exist = False
        print
        "have no " + input_dir + "\n"

    return [weight_unifrac_data_list, weight_unifrac_jqGrid_list, sampleName,
            exist]


def save_table2(input_dir):
    # save table
    # save table
    exist = True
    weight_unifrac_data_list = []
    weight_unifrac_jqGrid_list = []
    sampleName = "'"
    try:
        with open(input_dir) as lines:
            head = lines.next()
            head = html_translate(head)
            samples_name = head.strip().split('\t')
            if (len(samples_name) > 10):
                samples_name_two = samples_name[:10]
                sampleName = ("','").join(samples_name_two)
            else:
                sampleName = ("','").join(samples_name)
            jqGrid_head = "{name:'taxonname',index:'taxonname',width:140,align:'center'},"
            weight_unifrac_jqGrid_list.append(jqGrid_head)
            count = 0
            samples_name = samples_name[1:]
            for_time = []
            for i, value in enumerate(samples_name):
                for_time.append("%s%d" % ("sample", i))
            for line in lines:
                line = html_translate(line)
                count += 1

                tabs = line.strip().split("\t")
                str = "{taxonname:\"" + tabs[0] + "\","
                for i, value in enumerate(for_time):
                    jqGrid = '{'
                    if len(for_time) < 9:
                        if i < len(for_time) - 1:
                            str += '%s:"%s",' % (
                                value, stringasfloat(tabs[i + 1]))
                            # str += value+":\""+tabs[i+1]+"\","
                            jqGrid += "name:'" + value + "',index:'" + value + "',align:'center',width:90},"
                        else:
                            jqGrid += "name:'" + value + "',index:'" + value + "',align:'center',width:90}"
                            str += '%s:"%s"' % (
                                value, stringasfloat(tabs[i + 1]))
                            # str += value+":\""+tabs[i+1]+"\""
                            str += '},'
                    else:

                        if i < 8:
                            str += '%s:"%s",' % (
                                varlue, stringasfloat(tabs[i + 1]))
                            # str += value+":\""+tabs[i+1]+"\","
                            jqGrid += "name:'" + value + "',index:'" + value + "',align:'center',width:90},"
                        else:
                            jqGrid += "name:'" + value + "',index:'" + value + "',align:'center',width:90}"
                            str += '%s:"%s"' % (
                                value, stringasfloat(tabs[i + 1]))
                            # str += value+":\""+tabs[i+1]+"\""
                            str += '},'
                            break
                    if count == 1:
                        weight_unifrac_jqGrid_list.append(jqGrid)
                weight_unifrac_data_list.append(str)
            if count == 0:
                return [[], [], None, False]
    except IOError:
        exist = False
        print
        "have no " + input_dir + "\n"
    return [weight_unifrac_data_list, weight_unifrac_jqGrid_list, sampleName,
            exist]


def read_params(args):
    parser = argparse.ArgumentParser(description='get_html ')
    parser.add_argument('-c',
                        '--config',
                        dest='config',
                        metavar='FILE',
                        type=str,
                        required=True,
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
    work_dir = config.get('params', 'work_dir')
    out_dir_report = config.get('outfiles', 'out_dir')
    data_type = config.get('params', 'data_type')
    group_files = re.split('\s+', config.get('params', 'group_files'))
    group_file_origin = group_files[0]
    group_file = re.search('.+\/(.+)\..+', group_file_origin).group(1)

    # save table
    var_html = {}
    tabs = []
    otuStatisticals = {}
    with open(work_dir + "../" + config.get('origin', 'pick_otu_txt'),
              'r') as lines:
        var_html['sample_sum'] = int(lines.next().strip().split(":")[1])
        var_html['otu_sum'] = int(lines.next().strip().split(":")[1])
        lines.next()
        lines.next()
        lines.next()
        lines.next()
        for line in lines:
            tabs = line.strip().split("\t")
            # sample_name amplicon_type tags mapped_reads mapped_ratio
            otuStatistical = OtuStatistical(tabs[0], data_type, tabs[1],
                                            tabs[8], tabs[9], tabs[4], tabs[5],
                                            tabs[2], tabs[3], tabs[10])
            otuStatisticals[tabs[0]] = otuStatistical

            # save otu statistic table
    otuStatisticalDownsizes = {}
    with open(work_dir + "../" + config.get('origin', 'otu_all_downsize_txt'),
              'r') as lines:
        lines.next()
        for line in lines:
            tabs = line.strip().split('\t')
            downsize = tabs[1]
            otuStatisticalDownsize = OtuStatisticalDownsize(tabs[0], tabs[1],
                                                            tabs[2], tabs[3])
            otuStatisticalDownsizes[tabs[0]] = otuStatisticalDownsize

            # save tabel CoreMicrobiome
    coreMicrobiomes = {}
    var_html['core_otu_exists'] = True
    try:
        with open(work_dir + "../" + config.get(
                'origin', 'group_core_otu_txt').replace("#group", group_file),
                  'r') as lines:
            lines.next()
            count = 0
            for line in lines:
                count += 1
                tabs = line.strip().split("\t")
                coreMicrobiome = CoreMicrobiome(tabs[0], tabs[1], tabs[2])
                coreMicrobiomes[tabs[0]] = coreMicrobiome
            if count == 0:
                var_html['core_otu_exists'] = False
    except IOError:
        var_html['core_otu_exists'] = False
        sys.stderr.write('there is no core microbiomes!\n')

    # save otu assignment stat table
    otuAssignmentsStatisticals = {}
    with open(work_dir + "../" + config.get('origin', 'otu_statistic_txt'),
              'r') as lines:
        lines.next()
        for line in lines:
            tabs = line.strip().split('\t')
            otuAssignmentsStatistical = OtuAssignmentsStatistical(
                    tabs[0], stringasfloat(tabs[1]))
            otuAssignmentsStatisticals[tabs[0]] = otuAssignmentsStatistical

            # save alpha diversity table
    alpha_diversitys = {}
    with open(work_dir + "../" + config.get(
            'origin', 'group_alpha_statistic_txt').replace("#group", group_file),
              'r') as lines:
        lines.next()
        for line in lines:
            tabs = line.strip().split('\t')
            alpha_diversity = Alpha_diversity(
                    tabs[0], stringasfloat(tabs[1]), stringasfloat(tabs[2]),
                    stringasfloat(tabs[3]), stringasfloat(tabs[4]),
                    stringasfloat(tabs[5]), stringasfloat(tabs[6]))
            alpha_diversitys[tabs[0]] = alpha_diversity

            # save alpha diff table
    alpha_diversity_diffs = {}
    alpha_diff_exist = True
    try:
        with open(work_dir + "../" + config.get(
                'origin', 'group_alpha_markers_txt').replace("#group", group_file),
                  'r') as lines:
            lines.next()
            for line in lines:
                tabs = line.strip().split('\t')
                alpha_diversity = Alpha_diversity(
                        tabs[0], stringasfloat(tabs[1]), stringasfloat(tabs[2]),
                        stringasfloat(tabs[3]), stringasfloat(tabs[4]),
                        stringasfloat(tabs[5]), stringasfloat(tabs[6]))
                alpha_diversity_diffs[tabs[0]] = alpha_diversity
    except IOError:
        alpha_diff_exist = False
        print
        "have no group_alpha_markers_txt\n"

    # save_table
    beta_un_diversity = save_table(work_dir + "../" + config.get(
            'origin', 'group_beta_div_un_txt').replace("#group", group_file))
    # save_table
    beta_diversity = save_table(work_dir + "../" + config.get(
            'origin', 'group_beta_div_txt').replace("#group", group_file))
    # save_table
    diff_otu_marker = save_table2(work_dir + "../" + config.get(
            'origin', 'group_diff_otu_marker_p_txt').replace("#group", group_file))
    # save_table
    diff_genus_marker = save_table2(work_dir + "../" + config.get(
            'origin', 'group_diff_genus_marker_p_txt').replace("#group",
                                                               group_file))
    # save_table
    diff_taxall_marker = save_table2(work_dir + "../" + config.get(
            'origin', 'group_diff_taxall_marker_p_txt').replace("#group",
                                                                group_file))
    # save_table
    diff_phylum_marker = save_table2(work_dir + "../" + config.get(
            'origin', 'group_diff_phylum_marker_txt').replace("#group",
                                                              group_file))
    # save_table
    env = Environment(loader=FileSystemLoader(out_dir_report + 'js/',
                                              encoding='utf-8'),
                      autoescape=False)
    template = env.get_template('table_template.js')
    otuStatisticals = sorted(otuStatisticals.iteritems(),
                             key=operator.itemgetter(1),
                             reverse=True)
    otuStatisticalDownsizes = sorted(otuStatisticalDownsizes.iteritems(),
                                     key=operator.itemgetter(1),
                                     reverse=True)
    table = template.render(
            otuStatisticals=otuStatisticals,
            otuStatisticalDownsizes=otuStatisticalDownsizes,
            otuAssignmentsStatisticals=otuAssignmentsStatisticals,
            alpha_diversitys=alpha_diversitys,
            alpha_diversity_diffs=alpha_diversity_diffs,
            alpha_diff_exist=alpha_diff_exist,
            beta_diversity_data=beta_diversity[0],
            beta_diversity_jqGrid=beta_diversity[1],
            beta_diversity_sampleName=beta_diversity[2],
            beta_diversity_exist=beta_diversity[3],
            beta_un_diversity_data=beta_un_diversity[0],
            beta_un_diversity_jqGrid=beta_un_diversity[1],
            beta_un_diversity_sampleName=beta_un_diversity[2],
            beta_un_diversity_exist=beta_un_diversity[3],
            coreMicrobiomes=coreMicrobiomes,
            diff_otu_marker_data=diff_otu_marker[0],
            diff_otu_marker_jqGrid=diff_otu_marker[1],
            diff_otu_marker_sampleName=diff_otu_marker[2],
            diff_otu_marker_exist=diff_otu_marker[3],
            diff_genus_marker_data=diff_genus_marker[0],
            diff_genus_marker_jqGrid=diff_genus_marker[1],
            diff_genus_marker_sampleName=diff_genus_marker[2],
            diff_genus_marker_exist=diff_genus_marker[3],
            diff_taxall_marker_data=diff_taxall_marker[0],
            diff_taxall_marker_jqGrid=diff_taxall_marker[1],
            diff_taxall_marker_sampleName=diff_taxall_marker[2],
            diff_taxall_marker_exist=diff_taxall_marker[3],
            diff_phylum_marker_data=diff_phylum_marker[0],
            diff_phylum_marker_jqGrid=diff_phylum_marker[1],
            diff_phylum_marker_sampleName=diff_phylum_marker[2],
            diff_phylum_marker_exist=diff_phylum_marker[3])
    with open(work_dir + 'report/js/table.js', 'w') as fp:
        fp.write(table)
    # save_table
    env = Environment(loader=FileSystemLoader(out_dir_report + 'js/',
                                              encoding='utf-8'),
                      autoescape=False)
    template = env.get_template('table_template_pdf.js')
    otuStatisticals = sorted(otuStatisticals.iteritems(),
                             key=operator.itemgetter(1),
                             reverse=True)
    otuStatisticalDownsizes = sorted(otuStatisticalDownsizes.iteritems(),
                                     key=operator.itemgetter(1),
                                     reverse=True)
    table = template.render(
            otuStatisticals=otuStatisticals,
            otuStatisticalDownsizes=otuStatisticalDownsizes,
            otuAssignmentsStatisticals=otuAssignmentsStatisticals,
            alpha_diversitys=alpha_diversitys,
            alpha_diversity_diffs=alpha_diversity_diffs,
            alpha_diff_exist=alpha_diff_exist,
            beta_diversity_data=beta_diversity[0],
            beta_diversity_jqGrid=beta_diversity[1],
            beta_diversity_sampleName=beta_diversity[2],
            beta_diversity_exist=beta_diversity[3],
            beta_un_diversity_data=beta_un_diversity[0],
            beta_un_diversity_jqGrid=beta_un_diversity[1],
            beta_un_diversity_sampleName=beta_un_diversity[2],
            beta_un_diversity_exist=beta_un_diversity[3],
            coreMicrobiomes=coreMicrobiomes,
            diff_otu_marker_data=diff_otu_marker[0],
            diff_otu_marker_jqGrid=diff_otu_marker[1],
            diff_otu_marker_sampleName=diff_otu_marker[2],
            diff_otu_marker_exist=diff_otu_marker[3],
            diff_genus_marker_data=diff_genus_marker[0],
            diff_genus_marker_jqGrid=diff_genus_marker[1],
            diff_genus_marker_sampleName=diff_genus_marker[2],
            diff_genus_marker_exist=diff_genus_marker[3],
            diff_taxall_marker_data=diff_taxall_marker[0],
            diff_taxall_marker_jqGrid=diff_taxall_marker[1],
            diff_taxall_marker_sampleName=diff_taxall_marker[2],
            diff_taxall_marker_exist=diff_taxall_marker[3],
            diff_phylum_marker_data=diff_phylum_marker[0],
            diff_phylum_marker_jqGrid=diff_phylum_marker[1],
            diff_phylum_marker_sampleName=diff_phylum_marker[2],
            diff_phylum_marker_exist=diff_phylum_marker[3])
    with open(work_dir + 'report/js/table_pdf.js', 'w') as fp:
        fp.write(table)
    # finally_get_html

    #    sample_num_in_groups,min_sample_mun_in_groups,sample_num_total,group_num = parse_group(group_file_origin)
    var_html['amplification'] = data_type
    var_html['core_microbiome'] = len(coreMicrobiomes)
    var_html['star_picture_top'] = 10
    var_html['Phylogenetic_genus_top'] = 10
    var_html['diff_otus'] = len(diff_otu_marker[0])
    var_html['diff_genus'] = len(diff_genus_marker[0])
    var_html['diff_species'] = len(diff_taxall_marker[0])
    var_html['diff_phylum'] = len(diff_phylum_marker[0])
    var_html['diff_otu_marker_exist'] = diff_otu_marker[3]
    var_html['diff_genus_marker_exist'] = diff_genus_marker[3]
    var_html['diff_phylum_marker_exist'] = diff_phylum_marker[3]
    var_html['diff_taxall_marker_exist'] = diff_taxall_marker[3]
    cutoff_dir = config.get('params', 'cutoff')
    cutoff_config = ConfigParser.ConfigParser()
    cutoff_config.read(work_dir + "../" + cutoff_dir.replace("#group", group_file))
    var_html['p_value'] = cutoff_config.get("params", 'p_cutoff')
    var_html['LDA_cutoff'] = cutoff_config.get("params", 'LDA_cutoff')
    var_html['downsize'] = downsize

    sample_num_in_groups, \
    min_sample_num_in_groups, \
    sample_num_total, \
    group_num = parse_group(group_file_origin)

    var_html['group_num'] = group_num
    var_html['reads_statistical'] = True
    var_html['otu_statistical'] = True
    var_html['downsize_html'] = True

    var_html['star_picture'] = True
    if sample_num_total <= 3:
        var_html['star_picture'] = False

    if sample_num_total >= 4:
        var_html['uniFra_analysis_heatmap'] = True

    if sample_num_total >= 5:
        var_html['core_microbiome_html'] = True
        var_html['otu_pca'] = True
        var_html['otu_heatmap'] = True
        var_html['uniFra_analysis_pcoa'] = True
        var_html['uniFra_analysis_nmds'] = True
        if group_num >= 2:
            var_html['uniFra_analysis_anosim'] = True

    if 2 <= group_num <= 5:
        var_html['otu_venn'] = True

    var_html['rank_abundance'] = True
    var_html['alpha_diversity'] = True
    if sample_num_total >= 10:
        var_html['specaccum'] = True
    var_html['otu_tax_assignments'] = True
    var_html['otu_annotation_statistical'] = True
    var_html['tax_summary'] = True
    var_html['otu_krona'] = True
    var_html['phylogenetic_tree'] = False
    var_html['similarity_analysis'] = False
    if min_sample_num_in_groups >= 3 and group_num >= 2:
        var_html['alpha_diff'] = True
    var_html['lefse_enough'] = False
    if min_sample_num_in_groups >= 3 and group_num >= 2:
        var_html['lefse_enough'] = True
        LDA_png = config.get('origin', 'group_lefse_LDA_png').replace('#group', group_file)
        cmd_result = os.popen('file %s/../%s' % (work_dir, LDA_png)).read().strip().split(': ')[-1]
        if cmd_result == 'empty':
            var_html['lefse'] = False
        else:
            var_html['lefse'] = True
        var_html['diff_analysis'] = True
    if min_sample_num_in_groups >= 5 and group_num >= 2:
        var_html['diff_analysis_boxplot'] = True
    if min_sample_num_in_groups >= 5:
        var_html['alpha_diff_boxplot'] = True
    var_html['group_file'] = group_file
    html_dir = config.get('params', 'html_template')
    env = Environment(loader=FileSystemLoader(html_dir + '/templates',
                                              encoding='utf-8'))
    template = env.get_template('report.html')
    finally_html = template.render(var_html)
    with open(config.get('outfiles', 'report_html'), 'w') as fp:
        fp.write(finally_html)
    templetaPDF = env.get_template('pdf.html')
    pdf = templetaPDF.render(var_html)
    with open(config.get('outfiles', 'pdf_html'), 'w') as fp:
        fp.write(pdf)


if __name__ == '__main__':
    get_html()
