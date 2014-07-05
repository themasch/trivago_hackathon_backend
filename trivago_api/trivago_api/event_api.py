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
        
def eventful_events(query, location, begin, end):
    events = []
    query = strip_accents(query)
    location = strip_accents(location)
    date_range = dates_to_eventful_range(begin, end)
    payload = {
        "location": location,
        "date": date_range,
        "page_size": 25,
    }
    if query is not None and query != "None":
        payload["keywords"] = query
    logger.info("query to eventful api: %s" % pformat(payload))
    result = None
    try:
        result = eventful_api_client.call('/events/search', **payload)
#            location=location, keywords=query, date=date_range, page_size=25)
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
