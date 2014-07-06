# -*- encoding: utf-8 -*-
# Standard library imports
from __future__ import absolute_import
from pprint import pformat
import logging

# Imports from core django
from django.views.decorators.cache import cache_page

# Imports from third party apps

# Local imports
from . import eventful_api
from . import eventbrite_api
from .util import cache

logger = logging.getLogger(__name__)

@cache(600)
def get_results(query, location, begin, end):
    api_calls = [
        eventful_api.eventful_events,
        eventbrite_api.eventbrite_events,
    ]
    results = []
    for api_call in api_calls:
        results.extend(api_call(query, location, begin, end))
    return results
