#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
sample
"""

import inspect
from seleniumbase.SeleniumBase import SeleniumBase

class TestCaseSample(SeleniumBase):
    """
    Test Case Sample
    """
    target_uri = ''
    ss_path = './'

    def test_case_sample_01(self):
        """
        test_case_a_01
        """
        driver = self.driver
        driver.get(self.base_url + self.target_uri)
        func_name = inspect.currentframe().f_code.co_name

        # get access
        ss_name = '%s_01.png' % func_name
        driver.save_screenshot(self.ss_path + ss_name)

        # input search word
        self.input_text('q', 'python')
        ss_name = '%s_02.png' % func_name
        driver.save_screenshot(self.ss_path + ss_name)

        # click search button
        self.click_btn('input[type="submit"]')
        ss_name = '%s_03.png' % func_name
        driver.save_screenshot(self.ss_path + ss_name)
