# -*- encoding: utf-8 -*-
# Standard library imports
from __future__ import absolute_import
import unicodedata
from datetime import datetime
from hashlib import sha1
from django.core.cache import cache as _djcache

def strip_accents(s):
    return ''.join((c for c in unicodedata.normalize('NFD',
        unicode(s)) if unicodedata.category(c) != 'Mn'))

def date_to_str(date):
    return date.strftime("%Y%m%d%H%M%S")

def date_from_str(date_str):
    return datetime.strptime(date_str, "%Y%m%d%H%M%S")

def remap(raw_data, mapping):
    data = {}
    for k, (transform, v) in mapping:
        if transform is not None:
            val = raw_data.get(k)
            if val is not None:
                data[v] = transform(raw_data.get(k))
            else:
                data[v] = None
        else:
            data[v] = raw_data.get(k)
    return data

def cache(seconds=900):
    """
        Cache the result of a function call for the specified number of seconds, 
        using Django's caching mechanism.
        Assumes that the function never returns None (as the cache returns None to indicate a miss), and that the function's result only depends on its parameters.
        Note that the ordering of parameters is important. e.g. myFunction(x = 1, y = 2), myFunction(y = 2, x = 1), and myFunction(1,2) will each be cached separately. 

        Usage:

        @cache(600)
        def myExpensiveMethod(parm1, parm2, parm3):
            ....
            return expensiveResult
`
    """
    def doCache(f):
        def x(*args, **kwargs):
                key = sha1(str(f.__module__) + str(f.__name__) + str(args) + str(kwargs)).hexdigest()
                result = _djcache.get(key)
                if result is None:
                    result = f(*args, **kwargs)
                    _djcache.set(key, result, seconds)
                return result
        return x
    return doCache
