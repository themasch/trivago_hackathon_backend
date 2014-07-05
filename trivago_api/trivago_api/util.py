# -*- encoding: utf-8 -*-
# Standard library imports
from __future__ import absolute_import
from datetime import datetime

def date_to_str(date):
    return date.strftime("%Y%m%d%H%M%S")

def date_from_str(date_str):
    return datetime.strptime(date_str, "%Y%m%d%H%M%S")
