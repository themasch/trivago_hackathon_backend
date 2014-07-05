# -*- encoding: utf-8 -*-
# Standard library imports
from __future__ import absolute_import

# Imports from core django
from django.conf.urls import patterns, url, include

# Imports from third party apps
#from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

# Local imports
from . import views

urlpatterns = format_suffix_patterns(patterns('trivago_api.views',
    url(r'^$', 'api_root', name='api-root'),
    url(r'^events/$', views.EventList.as_view(), name='events'),
    url(r'^blockEvent/$', views.BlockEvent.as_view(), name='block-event'),
))

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
