# -*- encoding: utf-8 -*-
# Standard library imports
from __future__ import absolute_import
import logging
from pprint import pformat

# Imports from core django
from django.forms import widgets
from django.contrib.auth.models import User

# Imports from third party apps
from rest_framework import serializers

# Local imports
from trivago_api.models import Event

logger = logging.getLogger(__name__)

class TrivagoData(dict):

    def __init__(self, data, save_func=None):
        super(TrivagoData, self).__init__(**data)
        self.__dict__ = self
        self._save_func = save_func

    def save(self):
        self._save_func(self)


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ('url', 'titel', 'desc')

class SearchSerializer(serializers.Serializer):
    begin = serializers.DateField()
    end = serializers.DateField()
    query = serializers.CharField(required=False)
    location = serializers.CharField()

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.date_search = attrs.get('date_search', instance.date_search)
            instance.begin = attrs.get('begin', instance.begin)
            instance.end = attrs.get('end', instance.end)
            instance.query = attrs.get('query', instance.query)
            instance.location = attrs.get('location', instance.location)
            return instance

        instance = TrivagoData(attrs)
        logger.info("search serializer: %s" % pformat(instance))
        return instance
