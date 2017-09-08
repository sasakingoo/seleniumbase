#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
selenium and unit test base class
require PhantomJS
"""

import os
import base64
import urllib2
import httplib
import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class SeleniumBase(unittest.TestCase):
    """
    selenium and unit test base class
    """
    base_url = ''
    basic_auth = False
    user = ''
    password = ''
    conf = [
        '--ignore-ssl-errors=true',
        '--webdriver-loglevel=NONE'
    ]

    def setUp(self):
        if self.basic_auth:
            b64_account = base64.b64encode(b'%s:%s' % (self.user, self.password))
            authentication_token = "Basic %s" % b64_account
            capa = DesiredCapabilities.PHANTOMJS
            capa['phantomjs.page.customHeaders.Authorization'] = authentication_token
            self.driver = webdriver.PhantomJS(desired_capabilities=capa,
                                              service_args=self.conf,
                                              service_log_path=os.path.devnull)
        else:
            self.driver = webdriver.PhantomJS(service_args=self.conf,
                                              service_log_path=os.path.devnull)


    def tearDown(self):
        self.driver.quit()

    def input_text(self, name, text):
        """
        Args
            name: name attribute
            text: input string
        """
        script = "document.getElementsByName('%s')[0].value = '%s';" % (name, text)
        self.driver.execute_script(script)

    @classmethod
    def check_basic_auth(cls, url):
        """
        check basic auth
        Return:
            bool
        """
        try:
            urllib2.urlopen(url)
            return False
        except urllib2.HTTPError as http_err:
            if http_err.code == httplib.UNAUTHORIZED:
                return True
            return False

    @classmethod
    def run_suite(cls, dir_path, params=None):
        """
        test runner
        Args:
            dir_path (str): path with test case
            params (dict): parameters necessary for executing the test
        """
        if params:
            # base url orverwrite
            if 'base_url' in params:
                cls.base_url = params['base_url']
            # enable basic auth mode
            if 'basic_auth' in params:
                cls.basic_auth = params['basic_auth']
            # basic auth user orverwrite
            if 'user' in params:
                cls.user = params['user']
            # basic auth password orverwrite
            if 'password' in params:
                cls.password = params['password']

        pattern = params['pattern'] if 'pattern' in params else ''

        suite = unittest.loader.TestLoader().discover(dir_path, pattern)
        unittest.TextTestRunner(verbosity=2).run(suite)