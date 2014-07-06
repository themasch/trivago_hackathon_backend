# -*- encoding: utf-8 -*-
# Standard library imports
from __future__ import absolute_import
from pprint import pformat
import logging
import requests
import json
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date

# Imports from core django
from django.conf import settings

# Imports from third party apps

# Local imports
from .util import remap
#from .util import strip_accents

logger = logging.getLogger(__name__)

def date_from_eventbrite(item):
    date_obj = parse_date(item["utc"])
    date_obj.replace(tzinfo=None)
    return date_obj
    
def get_text(item):
    return item["text"]

def get_name(item):
    return item["name"]

def ticket_price(item):
    if len(item) > 0:
        return item[0].get("cost", {}).get("value")

def get_city(item):
    return item.get("address", {}).get("city")

def get_latitude(item):
    locstr = item.get("latitude")
    if locstr is not None:
        return float(locstr)
    else:
        return None
    
def get_longitude(item):
    locstr = item.get("longitude")
    if locstr is not None:
        return float(locstr)
    else:
        return None

EVENTBRITE_MAPPING = (
    ("id", (lambda x: "eventbrite_%s" % x, "id")),
    ("name", (get_text, "title")),
    ("description", (get_text, "desc")),
    ("venue", (get_name, "venue")),
    ("category", (get_name, "category_name")),
    ("logo_url", (None, "image")),
    ("logo_url", (None, "image_small")),
    ("ticket_classes", (ticket_price, "ticket_price")),
    ("organizer", (lambda x: x.get("url"), "venue_url")),
    ("venue", (get_city, "city")),
    ("venue", (lambda x: x.get("address", {}).get("country_name"), "country")),
    ("venue", (lambda x: x.get("address", {}).get("region"), "region")),
    ("url", (None, "url")),
    ("venue", (get_latitude, "lat")),
    ("venue", (get_longitude, "lng")),
    ("start", (date_from_eventbrite, "begin")),
    ("end", (date_from_eventbrite, "end")),
)

def eventbrite_to_trivago(item):
    #logger.info("eventbrite to trivago: %s" % pformat(item))
    event = remap(item, EVENTBRITE_MAPPING)
    #if item.get("image") is not None:
    #    event["image_small"] = item.get("image", {}).get("thumb", {}).get("url")
    #    event["image"] = item.get("image", {}).get("medium", {}).get("url")
    logger.info("eventbrite to trivago new: %s" % pformat(event))
    return event

API_URL = "https://www.eventbriteapi.com/v3/events/search/"
        
def eventbrite_events(query, location, begin, end):
    logger.info("eventbrite query: %s %s %s %s" % (query, location, begin, end))
    session = requests.Session()
    payload = {
        "token": settings.EVENTBRITE_OAUTH_TOKEN,
        "q": query,
        #"location.address": location,
        "venue.city": location,
        "start_date.range_start": begin.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "start_date.range_end": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    result = {}
    response = session.get(API_URL, params=payload)
    if response.status_code == requests.codes.ok:
        result = json.loads(response.content)
    #logger.info("eventbrite result: %s" % pformat(result))
    events = []
    if len(result.get("events")) > 0:
        for event in result["events"]:
            events.append(eventbrite_to_trivago(event))
    return events
