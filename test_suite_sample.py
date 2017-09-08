#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
run test suite:
    python -B test_suite.py

run test suite for basic auth:
    python -B test_suite.py -u user -p password

execute options:
    -u : basic auth user
    -p : basic auth password
"""

import sys
import argparse
from seleniumbase import SeleniumBase

# website base URL
BASE_URL = ''

def main():
    """
    main function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', metavar='user', type=str,
                        default='', help='basic auth user')
    parser.add_argument('-p', '--password', metavar='password', type=str,
                        default='', help='basic auth password')
    parser.add_argument('--base_url', metavar='base url', type=str,
                        default='', help='base url')
    args = parser.parse_args()

    base_url = BASE_URL if BASE_URL else args.base_url
    user = args.user
    password = args.password

    if not base_url:
        sys.exit('Please set the base URL of the website you want to test!')

    basic_auth = SeleniumBase.check_basic_auth(base_url)
    if basic_auth:
        if not user or not password:
            sys.exit('Please set the basic auth account of the website you want to test!')

    params = {
        'pattern': 'TestCase*',
        'base_url': base_url,
        'basic_auth': basic_auth,
        'user': user,
        'password': password
    }

    SeleniumBase.run_suite('test_case_sample', params)

if __name__ == '__main__':
    main()
