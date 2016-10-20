#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

from . import const
const.pipeline_dir = "/data_center_01/pipeline/16S_ITS_pipeline_v3.0/"
const.config = "%s/config/" % const.pipeline_dir
const.html_template_miseq = "/data_center_01/pipeline/16S_ITS_pipeline_v3.0/src/16S20160112"
const.html_template_hiseq = "/data_center_01/pipeline/16S_ITS_pipeline_v3.0/src/16S20161020-h"
const.html_template_jin = "/data_center_01/pipeline/16S_ITS_pipeline_v3.0/src/16S20160223-h-jin"