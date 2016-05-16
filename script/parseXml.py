#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"
import xlrd
import re
import  argparse
import sys

this_script_path = os.path.dirname(__file__)
sys.path.insert(1, this_script_path + '/../src')
import Parser as rp

def read_params(args):
    parser = argparse.ArgumentParser(description='group file change')
    parser.add_argument('-i', '--input', dest='input', metavar='input', type=str, required=True,
                        help="input file")
    parser.add_argument('-o', '--outputdir', dest='outputdir', metavar='outputdir', type=str,required=True,
                        help="out put dir")
    args = parser.parse_args()
    params = vars(args)
    return params
def len_list(rowvlaue):
    r_list = []
    samples_ncol = len(rowvalue)
    for value in rowvalue:
        if not value:
            samples_ncol -= 1
            continue
        value = value.encode('utf-8')
        r_list.append(value)
    return samples_ncol,r_list
if __name__ == '__main__':
    params = read_params(sys.argv)
    data = xlrd.open_workbook(params["input"])
    table = data.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols
    to_read_sample = False
    to_read_group = False
    newname = {}
    samples = {}
    groups = {}
    samples_read_num = 0
    groups_read_num = 0
    with open("%s/outgroup.txt"%params["outputdir"],"w") as fqout , open("%s/outgroupname.txt" % params["outputdir"],"w") as fqout2:
        for i in range(nrows):

            if re.search("^四、分组信息",table.cell_value(i,0).encode('utf-8')):
                to_read_sample = True
            if re.search("^五、比较方案*",table.cell_value(i,0).encode('utf-8')):
                to_read_group = True
                to_read_sample = False
            if to_read_sample:
                if samples_read_num <= 1 :
                    rowvalue = table.row_values(i)
                    samples_ncol =len_list(rowvalue)
                    samples_read_num += 1
                else:
                    rowvalue = table.row_values(i)
                    len_value,r_list =len_list(rowvalue)
                    if len_value <= 2:
                        continue
                    else:
                        fqout.write("\t".join(r_list))
                        fqout.write("\n")
            if to_read_group:
                if groups_read_num <= 1:
                    rowvalue = table.row_values(i)
                    groups_ncol =len_list(rowvalue)
                    groups_read_num += 1
                else:
                    rowvalue = table.row_values(i)
                    len_value,r_list =len_list(rowvalue)
                    if len_value <= 2:
                        to_read_group = False
                        continue
                    else:
                        fqout2.write("\t".join(r_list))
                        fqout2.write("\n")

    r_job = rp.Rparser()
    r_job.open(this_script_path + '/../src/template/parseGroup.Rtp')
    file_group = "%s/outgroup.txt"%params["outputdir"]
    file_group_name = "%s/outgroupname.txt" % params["outputdir"]
    file_R = '%s/parseGroup.R' % (params["outputdir"])
    vars_in = {'file_group': file_group,
               'file_group_name': file_group_name,
               'outputdir':params["outputdir"]
               }
    r_job.format(vars_in)
    r_job.write(file_R)
    r_job.run()