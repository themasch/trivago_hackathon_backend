# -*- encoding: utf-8 -*-
# Standard library imports
from __future__ import absolute_import
import logging

# Imports from core django
from django.db import models

# Imports from third party apps
from rest_framework import serializers

# Local imports

logger = logging.getLogger(__name__)

class Event(models.Model):
    titel = models.CharField(max_length=255)
    description = models.CharField(max_length=512)
    url = models.URLField()
