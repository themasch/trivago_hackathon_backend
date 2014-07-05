# -*- encoding: utf-8 -*-

from __future__ import absolute_import

import os
import sys
import logging

from joblib import Memory
from pprint import pprint
from csv import DictReader
from datetime import datetime, date

from .config import paths

logger = logging.getLogger(__name__)
memory = Memory(cachedir=paths.cache)

fieldnames=None

class HackathonParser(object):
    def __init__(self):
        self.float_fields = ["latitude_search", "latitude_user",
            "longitude_search", "longitude_user"]
        self.search_date_fields = ["year_search", "month_search", "day_search"]

    def parse_dates(self, row):
        search_dateints = [int(row[x]) for x in self.search_date_fields]
        search_date = date(*search_dateints)
        row["search_date"] = search_date
        for key in self.search_date_fields:
            del row[key]
        arrival = datetime.strptime(row["arrival"], "%Y%m%d").date()
        row["arrival"] = arrival
        departure = datetime.strptime(row["departure"], "%Y%m%d").date()
        row["departure"] = departure
        return row

    def parse_floats(self, row):
        for float_field in self.float_fields:
            row[float_field] = float(row[float_field])
        return row

    def parse(self, row_id, row):
        row = self.parse_dates(row)
        row = self.parse_floats(row)
        row["id"] = row_id
        return row


def _lines_from_csv():
    """ read trivago csv hackathon data """
    print(paths.queries)
    fieldnames = [
        "year_search",
        "month_search",
        "day_search",
        "platform_search",
        "city_search",
        "country_search",
        "continent_search",
        "longitude_search",
        "latitude_search",
        "arrival",
        "departure",
        "group_search",
        "city_user",
        "country_user",
        "continent_user",
        "longitude_user",
        "latitude_user",
    ]
    with open(paths.queries) as query_file:
        for num, row in enumerate(DictReader(query_file, fieldnames=fieldnames)):
            if num > 0 and num % 100000 == 0:
                logger.info("%s %s" % (paths.queries, num))
            yield row
        query_file.close()

@memory.cache
def parse_hackathon():
    hp = HackathonParser()
    data = []
    for row_id, row in enumerate(_lines_from_csv()):
        row = hp.parse(row_id, row)
        #pprint(row)
        data.append(row)
    return data
