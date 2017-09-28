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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

DEFAULT_WAIT_TIME = 10

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

        self.driver.implicitly_wait(DEFAULT_WAIT_TIME)

    def tearDown(self):
        self.driver.quit()

    def input_text(self, name, text):
        """
        Args
            name (str): name attribute
            text (str): input string
        """
        script = "document.getElementsByName('%s')[0].value = '%s';" % (name, text)
        self.driver.execute_script(script)

    def click_btn(self, locator):
        """
        Args
            locator (str): css selector
        """
        btn = self.driver.find_element_by_css_selector(locator)
        btn.click()

    def click_radio(self, name, value):
        """
        Args:
            name (str): name attribute
            value (str): Value want to select
        """
        locator = 'input[name="%s"][value="%s"]' % (name, value)
        radio_btn = self.driver.find_element_by_css_selector(locator)
        radio_btn.click()

    def wait_for_enabled(self, locator):
        """
        waiting for element enabled
        Args:
            locator (str): css selector
        Return:
            bool
        """
        try:
            elm = WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, locator))
            )
            return elm.is_enabled()
        except NoSuchElementException:
            self.driver.save_screenshot('wait_for_enabled_failed.png')
            return False

    def wait_for_disabled(self, locator):
        """
        waiting for element disabled
        Args:
            locator (str): css selector
        Return:
            bool
        """
        try:
            elm = WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until_not(
                EC.element_to_be_clickable((By.CSS_SELECTOR, locator))
            )
            return not elm.is_enabled()
        except NoSuchElementException:
            self.driver.save_screenshot('wait_for_disabled_failed.png')
            return False

    def wait_for_text_present(self, locator, text):
        """
        waiting for text present
        Args:
            locator (str): css selector
            text (str): string to compare
        Return:
            bool
        """
        try:
            WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, locator), text)
            )
        except NoSuchElementException:
            self.driver.save_screenshot('wait_for_text_present_failed.png')

    @classmethod
    def check_basic_auth(cls, url):
        """
        check basic auth
        Return:
            bool
        """
        try:
            urllib2.urlopen(url)
        except urllib2.HTTPError as http_err:
            if http_err.code == httplib.UNAUTHORIZED:
                return True
        except urllib2.URLError:
            return False
        else:
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
