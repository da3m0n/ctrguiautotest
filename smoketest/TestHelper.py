import os
from smoketest.mylib.utils import Utils


def make_sure_path_exists(path):
    import errno

    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


class TestHelper(object):
    def __init__(self, log, driver):
        self.log_dir = Utils.log_dir()
        self.driver = driver
        self.log = log
        self.error_count = 0

    def assert_true(self, val, msg=None, test_name=None):
        if val:
            self.error_count += 1
            pwd = os.getcwd()
            screenshots_dir = pwd + '\\logs\\' + self.log.url_friendly_start + '\\screenshots'

            if make_sure_path_exists(screenshots_dir):
                os.mkdir('screenshots')
                os.chdir(screenshots_dir)
                self.driver.save_screenshot(test_name + '.png')
            else:
                os.chdir(screenshots_dir)
                self.driver.save_screenshot(test_name + '.png')
            os.chdir(pwd)
            self.log.log_it2(self.error_count, msg, test_name)
        else:
            msg = '-'
            # self.driver.save_screenshot('testypass.png')
            self.log.log_it2(self.error_count, msg, test_name)

    def assert_not_equal(self, val1, val2, msg=None):
        if val1 != val2:
            self.errorCount += 1
            res = {'expected': val2, 'detected': val1}
            self.log.log_it(res)
