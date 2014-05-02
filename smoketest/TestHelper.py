class TestHelper(object):
    def __init__(self, log):
        self.log = log
        self.errorCount = 0

    def assert_true(self, val, msg=None, testName=None):
        if val:
            self.errorCount += 1
            # res = {'errorCount': str(self.errorCount), 'msg': msg}
            self.log.log_it2(self.errorCount, msg, testName)
        else:
            msg = '-'
            self.log.log_it2(self.errorCount, msg, testName)


def assertNotEqual(self, val1, val2, msg=None):
    if val1 != val2:
        self.errorCount += 1
        res = {'expected': val2, 'detected': val1}
        self.log.log_it(res)
