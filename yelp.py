#!/usr/bin/python

import requests
import argparse
import sys
import os
import urllib

from urllib import quote

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir+"/inc")

from constants import *


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
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
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
    info = search(args.term, args.location)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                            type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                            default=DEFAULT_LOCATION, type=str,
                            help='Search location (default: %(default)s)')

    args= parser.parse_args()
    main(args)
