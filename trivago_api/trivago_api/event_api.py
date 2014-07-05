# -*- encoding: utf-8 -*-
# Standard library imports
from __future__ import absolute_import
from pprint import pformat
import logging
from datetime import datetime, timedelta

# Imports from core django
from django.conf import settings

# Imports from third party apps
import eventful

# Local imports
from .util import remap

logger = logging.getLogger(__name__)

def date_from_eventful_str(date_str):
    if date_str is not None:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    else:
        return None

eventful_api_client = eventful.API(settings.EVENTFUL_API_KEY)

EVENTFUL_MAPPING = {
    "title": (None, "title"),
    "description": (None, "desc"),
    "venue_name": (None, "venue"),
    "venue_url": (None, "venue_url"),
    "city_name": (None, "city"),
    "country_name": (None, "country"),
    "region_name": (None, "region"),
    "url": (None, "url"),
    "latitude": (float, "lat"),
    "longitude": (float, "lng"),
    "start_time": (date_from_eventful_str, "begin"),
    "stop_time": (date_from_eventful_str, "end")
}

def eventful_to_trivago(item):
    logger.info("item: %s" % pformat(item))
    event = remap(item, EVENTFUL_MAPPING)
    logger.info("image: %s" % pformat(item.get("image")))
    if item.get("image") is not None:
        logger.info("item: %s" % pformat(item.get("image", {}).get("thumb", {}).get("url")))
        event["image_small"] = item.get("image", {}).get("thumb", {}).get("url")
        event["image"] = item.get("image", {}).get("medium", {}).get("url")
    return event
        
def eventful_events(query, begin, end):
    events = []
    result = eventful_api_client.call('/events/search', keywords=query)
    eventful_events = result["events"]["event"]
    for item in eventful_events:
        events.append(eventful_to_trivago(item))
        #events.append(item)
    return events
