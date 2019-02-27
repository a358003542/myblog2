#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://docs.cdwanze.work'
RELATIVE_URLS = False

DELETE_OUTPUT_DIRECTORY = False

# Following items are often useful when publishing

## add disqus comment
DISQUS_SITENAME = 'cdwanzes-blog'

GOOGLE_ANALYTICS = "UA-80598120-2"