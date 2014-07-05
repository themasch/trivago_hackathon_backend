# -*- encoding: utf-8 -*-
# Standard library imports
from __future__ import absolute_import

import json
from datetime import datetime

def date_to_str(date):
    return date.strftime("%Y%m%d%H%M%S")

def date_from_str(date_str):
    return datetime.strptime(date_str, "%Y%m%d%H%M%S")

def query_to_json(query):
    date_fields = ["arrival", "departure", "search_date"]
    for df in date_fields:
        query[df] = date_to_str(query[df])
    return json.dumps(query)
