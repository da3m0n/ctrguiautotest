class TestHelper(object):

    def __init__(self, log):
        self.log = log
        self.errorCount = 0

    def assertTrue(self, val, msg=None):
        if not val:
            self.errorCount += 1
            # self.log.log_it2(self.errorCount, msg)
            res = {'errorCount': str(self.errorCount), 'msg': msg}
            # self.log.log_it(res)

            self.log.log_it2(self.errorCount, msg)

    def assertNotEqual(self, val1, val2, msg=None):
        if val1 != val2:
            self.errorCount += 1
            res = {'expected': val2, 'detected': val1}
            self.log.log_it(res)
