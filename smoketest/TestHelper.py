from smoketest.mylib.utils import Utils


class TestHelper(object):
    def __init__(self, log, driver):
        self.log_dir = Utils.log_dir()
        self.driver = driver
        self.log = log
        self.error_count = 0

    def assert_true(self, val, msg=None, test_name=None):
        print('testName', test_name)
        if val:
            self.error_count += 1
            # res = {'errorCount': str(self.errorCount), 'msg': msg}
            self.driver.save_screenshot('testy.png')
            self.log.log_it2(self.error_count, msg, test_name)
        else:
            msg = '-'
            self.driver.save_screenshot('testypass.png')
            self.log.log_it2(self.error_count, msg, test_name)

    def assert_not_equal(self, val1, val2, msg=None):
        if val1 != val2:
            self.errorCount += 1
            res = {'expected': val2, 'detected': val1}
            self.log.log_it(res)
