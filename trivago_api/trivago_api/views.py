# -*- encoding: utf-8 -*-
# Standard library imports
from __future__ import absolute_import
from pprint import pformat
import logging
from datetime import datetime, timedelta

# Imports from core django

# Imports from third party apps
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# Local imports
from .serializers import EventSerializer
from .serializers import SearchSerializer
from .util import date_from_str
from . import event_api

logger = logging.getLogger(__name__)

@api_view(('GET',))
def api_root(request, format=None):
    """
    Api Root, *markdown* should work _foo_
    """
    public = {
        'events': reverse('events', request=request, format=format),
    }
    links = public
    return Response(links)


class EventList(APIView):
    """ Search for events -> list of events
    """
    def get_defaults(self):
        data = {}
        begin = datetime.now() + timedelta(days=14)
        end = begin + timedelta(days=3)
        data["begin"] = begin
        data["end"] = end
        return data

    def cleanup_params(self, query_params):
        params = {}
        for name, val in query_params.iteritems():
            if name in ("begin", "end"):
                params[name] = date_from_str(val)
            elif name in ("query",):
                params[name] = val
        return params

    def get(self, request, format=None):
        data = self.get_defaults()
        data.update(self.cleanup_params(request.QUERY_PARAMS))
        serializer = SearchSerializer(data=data)
        logger.info("search for events %s" % pformat(data))
        query, begin, end = [data.get(k) for k in ("query", "begin", "end")]
        events = []
        if serializer.is_valid():
            logger.info("heureka")
            events = event_api.eventful_events(query, begin, end)
        return Response(events)

class CatList(APIView):
    """ List of categories
    """
    def get(self, request, format=None):
	cats = event_api.eventful_cats()
	return Response(cats)	
