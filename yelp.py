#!/usr/bin/python

from __future__ import print_function

import requests
import argparse
import sys
import os
import urllib

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir+"/inc")

API_KEY = 'LauOYSu4b1p9NpsDjYaSVsq-vezHUKm_6l0Ne46oxGTaUYSzqaT-9o4KPFSGwyzFel_3EBk3oQqJBcFRIbaHp-kXVoKUL-tZQByhVn71buU8-x-9UktUVrupN9FAXXYx'
CLIENT_ID = 'S6VpuasaZLqlmTFRpH5F2A'

# API constants. Should not need to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


DEFAULT_LOCATION = 'San Jose, CA'
DEFAULT_TERM = 'dinner'

SEARCH_LIMIT = 3


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, urllib.quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(term, location):
    """ Search for entity given args

    Args:
        term: name, business, etc.
        location: city and state

    Return:
        Result of search
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ','+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, API_KEY, url_params=url_params)


def main(args):
    rc = 0
    term = args.term
    location = args.location

    info = search(term, location)

    businesses = info.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        rc = 1
        return rc

    print('%20s, %10s, %10s, %10s, %60s, %15s' % ("Name", "Rating", "Review Count", "Price", "Address", "Closed"))

    for business in businesses:
        #import pdb; pdb.set_trace()
        name = business.get('name')
        rating = business.get('rating')
        review_count = business.get('review_count')
        price = business.get('price')
        location= business.get('location')
        address = ' '.join(location.get('display_address'))
        is_closed = business.get('is_closed')

        print('%20s, %10s, %10s, %10s, %60s, %15s' % (name, rating, review_count, price, address, is_closed))






if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                            type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                            default=DEFAULT_LOCATION, type=str,
                            help='Search location (default: %(default)s)')

    args= parser.parse_args()
    main(args)
