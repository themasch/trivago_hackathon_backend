# -*- encoding: utf-8 -*-
# Standard library imports
from __future__ import absolute_import
from pprint import pformat
import logging

# Imports from core django

# Imports from third party apps
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# Local imports
from trivago_api.serializers import EventSerializer

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
    """
    Event list
    """

    def get(self, request, format=None):
        logger.info("serch for events %s" % pformat(request.QUERY_PARAMS))
        return Response({"foobar": "baz"})
