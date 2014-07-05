# -*- encoding: utf-8 -*-

import json
import logging
import requests
import argparse

from pprint import pprint
from urlparse import urljoin
from datetime import datetime, timedelta

try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

class RestUrls(object):
    def __init__(self, base_url):
        self.events = urljoin(base_url, "events")

def test_get_events(events_url):
    test_query = {"arrival": "20110409000000", "longitude_user": 10.45, "latitude_user": 51.2167, "group_search": "1", "continent_search": "Europe", "city_user": "M\u00fchlhausen", "search_date": "20110330000000", "continent_user": "Europe", "departure": "20110410000000", "latitude_search": 40.416981, "city_search": "Madrid", "country_user": "Germany", "longitude_search": -3.703362, "country_search": "Spain", "id": 0, "platform_search": "DE"}
    response = requests.get(events_url, params=test_query)
    result = json.loads(response.content)
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="run tests against given url")
    args = parser.parse_args()
    rest_urls = RestUrls(args.url)
    events = test_get_events(rest_urls.events)
    pprint(events)

if __name__ == '__main__':
    main()
