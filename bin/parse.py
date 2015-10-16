#!/usr/bin/env python
# -*- coding: utf-8 -*- #

def parse_group(group_file):
    sample_set = set()
    group_set = {}
    with open(group_file) as group:
        for line in group:
            sample_name,group_name = line.strip().split('\t')
            if group_name not in group_set:
                group_set[group_name] = set()
            group_set[group_name].add(sample_name)
            sample_set.add(sample_name)
    sample_num_in_groups = map(lambda s:len(s),group_set)
    min_sample_num_in_groups= min(sample_num_in_groups)
    sample_num_total = len(sample_set)
    group_num = len(group_set)
    return sample_num_in_groups,min_sample_num_in_groups,sample_num_total,group_num

def parse_stat_file(stat_file,group_file=None):
    used_samples = set()
    used_samples = set()
    if group_file is not None:
        with open(group_file) as g:
            for line in g:
                used_samples.add(line.split('\t')[0])
    with open(stat_file) as fp:
        line = fp.next()
        while(line):
            line = fp.next().strip()
        fp.next()
        maximum = 0
        minimum = 0xffffff
        for line in fp:
            tabs = line.strip().split('\t')
            if used_samples and tabs[0] not in used_samples:
                continue
            if maximum < int(tabs[1]):
                maximum = int(tabs[1])
            if minimum > int(tabs[2]):
                minimum = int(tabs[2])
    return maximum,minimum

