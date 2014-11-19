import os
from aurorasmoketest.mylib.utils import Utils


class TestHelper(object):
    def __init__(self, driver):
        self.driver = driver
        self.error_count = 0

    def assert_true(self, val, msg=None, test_name=None):
        if val:
            self.error_count += 1
            utils = Utils(self.driver)
            utils.save_screenshot(test_name)
        else:
            msg = '-'
            # self.driver.save_screenshot('testypass.png')
        self.error_count = 0

    def assert_not_equal(self, val1, val2, msg=None):
        if val1 != val2:
            self.errorCount += 1
            res = {'expected': val2, 'detected': val1}
