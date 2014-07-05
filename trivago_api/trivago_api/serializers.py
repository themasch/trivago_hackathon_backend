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

class TrivagoData(dict):

    def __init__(self, data, save_func=None):
        super(TrivagoData, self).__init__(**data)
        self.__dict__ = self
        self._save_func = save_func

    def save(self):
        self._save_func(self)


class EventSerializer(serializers.HyperlinkedModelSerializer):
    date_search = serializers.DateField()
    arrival = serializers.DateField()
    departure = serializers.DateField()
    lat_user = serializers.FloatField()
    lng_user = serializers.FloatField()
    lat_search = serializers.FloatField()
    lng_search = serializers.FloatField()
    group_search = serializers.BooleanField()

    class Meta:
        model = Event
        fields = ('url', 'titel', 'desc')

class SearchSerializer(serializers.Serializer):
    date_search = serializers.DateField()
    arrival = serializers.DateField()
    departure = serializers.DateField()
    lat_user = serializers.FloatField()
    lng_user = serializers.FloatField()
    lat_search = serializers.FloatField()
    lng_search = serializers.FloatField()
    group_search = serializers.BooleanField()
    city_search = CharField()
    city_user = CharField()
    continent_search = CharField()
    continent_user = CharField()
    country_search = CharField()
    country_user = CharField()
    platform_search = CharField()

    def restore_object(self, attrs, instance=None):
        from pprint import pformat
        logger.info("instance: %s" % pformat(instance))
        logger.info("attrs data: %s" % pformat(attrs))
        if instance is not None:
            instance.date_search = attrs.get('date_search', instance.date_search)
            instance.arrival = attrs.get('arrival', instance.arrival)
            instance.departure = attrs.get('departure', instance.departure)
            instance.lat_user = attrs.get('lat_user', instance.lat_user)
            instance.lng_user = attrs.get('lng_user', instance.lng_user)
            instance.lat_search = attrs.get('lat_search', instance.lat_search)
            instance.lng_search = attrs.get('lng_serach', instance.lng_search)
            instance.city_search = attrs.get('city_search', instance.city_search)
            instance.city_user = attrs.get('city_user', instance.city_user)
            instance.continent_search = attrs.get('continent_search', instance.continent_search)
            instance.continent_user = attrs.get('continent_user', instance.continent_user)
            instance.country_search = attrs.get('country_search', instance.country_search)
            instance.country_user = attrs.get('country_user', instance.country_user)
            instance.platform_search = attrs.get('platform_search', instance.platform_search)
            return instance

        instance = TrivagoData(attrs)
        logger.info("search serializer: %s" % pformat(instance))
        return instance
