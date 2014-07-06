# -*- encoding: utf-8 -*-
# Standard library imports
from __future__ import absolute_import
from pprint import pformat
import logging
from datetime import datetime, timedelta

# Imports from core django
from django.views.decorators.cache import cache_page

# Imports from third party apps
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# Local imports
from .serializers import EventSerializer
from .serializers import SearchSerializer
from .serializers import ItemIdSerializer
from .util import date_from_str
from . import search_api

logger = logging.getLogger(__name__)

@api_view(('GET',))
def api_root(request, format=None):
    """
    Api Root, *markdown* should work _foo_
    """
    public = {
        'search': reverse('search', request=request, format=format),
        'blockEvent': reverse('block-event', request=request, format=format),
    }
    links = public
    return Response(links)


class ResultList(APIView):
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
            elif name in ("query", "location"):
                params[name] = val
        return params
    
    def filter_excluded(self, items, excluded_ids):
        filtered_items = []
        for item in items:
            if item["id"] not in excluded_ids:
                filtered_items.append(item)
        return filtered_items

    def sort_results(self, results):
        results.sort(key=lambda item: item["begin"].strftime("%Y%m%d%H%M%S"))
        return results

    def get(self, request, format=None):
        data = self.get_defaults()
        data.update(self.cleanup_params(request.QUERY_PARAMS))
        serializer = SearchSerializer(data=data)
        logger.info("search for events %s" % pformat(data))
        query, location, begin, end = [data.get(k) for k in ("query", "location", "begin", "end")]
        logger.info("search for events %s %s %s %s" % (query, location, begin, end))
        events = []
        if serializer.is_valid():
            results = search_api.get_results(query, location, begin, end)
            excluded_ids = request.session.get("excluded_ids", {})
            results = self.filter_excluded(results, excluded_ids)
            results = self.sort_results(results)
            return Response(results)
        else:
            logger.info("serializer error: %s" % serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlockItem(APIView):
    """ Exclude Event with ID from listing
    """
    def post(self, request, format=None):
        serializer = ItemIdSerializer(data=request.DATA)
        if serializer.is_valid():
            excluded_ids = request.session.get("excluded_ids", {})
            excluded_ids[serializer.data["item_id"]] = True
            request.session["excluded_ids"] = excluded_ids
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.info("serializer error: %s" % serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
