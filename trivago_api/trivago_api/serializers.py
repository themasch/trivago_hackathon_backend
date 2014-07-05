# -*- encoding: utf-8 -*-
# Standard library imports
from __future__ import absolute_import
import logging

# Imports from core django
from django.forms import widgets
from django.contrib.auth.models import User

# Imports from third party apps
from rest_framework import serializers

# Local imports
from trivago_api.models import Event

logger = logging.getLogger(__name__)


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ('url', 'titel', 'desc')
