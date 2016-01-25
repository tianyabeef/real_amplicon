from __future__ import division
import re
import os
import sys
import copy
from Work import Work,Pipeline,SubWork,MyConfigParser
from parse import parse_group,parse_stat_file
this_script_path = os.path.dirname(__file__)
FUNCTIONAL_SCRIPT_DIR = this_script_path
DEFAULT_CONFIG_DIR = this_script_path  + '/../config'
sys.path.insert(1, this_script_path + '/../src')
from Parser import parse_group_file