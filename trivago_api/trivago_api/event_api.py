# -*- encoding: utf-8 -*-
# Standard library imports
from __future__ import absolute_import
from pprint import pformat
import logging
from datetime import datetime, timedelta
from urllib import urlencode

# Imports from core django
from django.conf import settings

# Imports from third party apps
import eventful

# Local imports
from .util import remap
from .util import strip_accents

logger = logging.getLogger(__name__)

def date_from_eventful_str(date_str):
    if date_str is not None:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    else:
        return None

def dates_to_eventful_range(begin, end):
    return "%s-%s" % (begin.strftime("%Y%m%d00"), end.strftime("%Y%m%d00"))

eventful_api_client = eventful.API(settings.EVENTFUL_API_KEY)

EVENTFUL_MAPPING = {
    "id": (None, "id"),
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
    event = remap(item, EVENTFUL_MAPPING)
    if item.get("image") is not None:
        event["image_small"] = item.get("image", {}).get("thumb", {}).get("url")
        event["image"] = item.get("image", {}).get("medium", {}).get("url")
    return event
        
def eventful_events(query, begin, end):
    events = []
    query = strip_accents(query)
    date_range = dates_to_eventful_range(begin, end)
    logger.info("query to eventful api: %s %s" % (query, date_range))
    try:
        result = eventful_api_client.call('/events/search',
            location=query, date=date_range, page_size=25)
    except Exception, err:
        logger.error("eventful api exception: %s" % pformat(err))
    if result is not None:
        event_dict = result.get("events", {})
        if event_dict is not None:
            eventful_events = event_dict.get("event", [])
            for item in eventful_events:
                events.append(eventful_to_trivago(item))
                #events.append(item)
    logger.info("got %s events" % len(events))
    return events

def eventful_cats():
    eventful_cats = {}
    logger.info("retrieve category list from eventful");
    try:
	result = eventful_api_client.call('/categories/list')
    except Exception, err:
	logger.error("eventful api exception: %s" % pformat(err))
    if result is not None:
	cat_dicts = result.get("category", {})
	if cat_dicts is not None:
	    for cat in cat_dicts:
		eventful_cats[cat["id"]] = cat["name"]
    logger.info("got %s cats" % len(eventful_cats))
    return eventful_cats

