from __future__ import division
import re
import os
import sys
from Work import Work,Pipeline,SubWork,MyConfigParser
this_script_path = os.path.dirname(__file__)
FUNCTIONAL_SCRIPT_DIR = this_script_path
DEFAULT_CONFIG_DIR = this_script_path  + '/../config'
