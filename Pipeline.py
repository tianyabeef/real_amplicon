from __future__ import division
import re
import os
import sys
this_script_path = os.path.dirname(__file__)
sys.path.insert(1,this_script_path + '/bin')

from work_00 import work_00_merge
from work_01 import work_01_pick_otu,work_01_alpha_rare
