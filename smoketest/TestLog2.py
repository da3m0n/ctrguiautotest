import time
from smoketest.mylib.utils import Utils


class TestLog(object):
    overall_errors = 0
    num_tests_run = 0
    name = ''

    def __init__(self):
        """Class to log errors"""
        # Utils.delete_existing_logfile('testLog.log')
        self.log = None
        print('Creating testLog...')
        self.per_test_errors = 0

    def start(self, name):
        self.name = name
        timetup = time.localtime()
        iso = time.strftime('%Y-%m-%d %H:%M:%S ', timetup)
        self.log = open('logs/output/testLog.log', 'a')
        self.log.write('========= Running ' + name + ' Tests\n')
        self.log.write('Started tests at ' + iso + '\n')
        self.num_tests_run += 1

    def log_it(self, data):
        self.log.write('   - ' + data + '\n')

    def end_log(self, error_count):
        self.per_test_errors = error_count

        if error_count == 0:
            self.log.write('========= Tests Passed. End ' + self.name + '\n')
        else:
            self.log.write('- ' + str(error_count) + ' failures.\n')
            self.log.write('========= End ' + self.name + ' tests.\n')
            self.overall_errors += 1

    def close(self):
        self.log.write('All Tests Finished. ' + str(self.num_tests_run) + ' Screen Tests run. ' + str(
            self.overall_errors) + ' Tests failed.\n')
        self.log.write('\n')
        self.log.close()