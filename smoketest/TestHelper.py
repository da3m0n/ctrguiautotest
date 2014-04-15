class TestHelper(object):

    def __init__(self, log):
        self.log = log
        self.errorCount = None

    def assertTrue(self, val, msg):
        if not val:
            self.errorCount += 1
            self.log.log_it2(self.errorCount, msg)
            res = {'errorCount': self.errorCount, 'msg': msg}
            self.log.log_it(res)

    def assertEquals(self, val1, val2):
        if val1 != val2:
            self.errorCount += 1
            self.log.log_it2()
