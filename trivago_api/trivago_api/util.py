# -*- encoding: utf-8 -*-
# Standard library imports
from __future__ import absolute_import
import unicodedata
from datetime import datetime

def strip_accents(s):
    return ''.join((c for c in unicodedata.normalize('NFD',
        unicode(s)) if unicodedata.category(c) != 'Mn'))

def date_to_str(date):
    return date.strftime("%Y%m%d%H%M%S")

def date_from_str(date_str):
    return datetime.strptime(date_str, "%Y%m%d%H%M%S")

def remap(raw_data, mapping):
    data = {}
    for k, (transform, v) in mapping.iteritems():
        if transform is not None:
            val = raw_data.get(k)
            if val is not None:
                data[v] = transform(raw_data.get(k))
            else:
                data[v] = None
        else:
            data[v] = raw_data.get(k)
    return data
