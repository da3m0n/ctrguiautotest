import time
from smoketest.mylib.utils import Utils


class TestLog(object):
    overall_errors = 0
    num_tests_run = 0

    def __init__(self, name):
        """Class to log errors"""
        # Utils.delete_existing_logfile('testLog.log')
        print('Creating testLog...')
        self.per_test_errors = 0
        self.num_tests_run += 1
        self.log = open('testLog.log', 'a')
        self.name = name

    def start(self):
        timetup = time.localtime()
        iso = time.strftime('%Y-%m-%d %H:%M:%S ', timetup)
        self.log.write('========= Running' + self.name + ' Tests\n')
        self.log.write('Started tests at ' + iso + '\n')

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
        self.log.write('All Tests Finished. ' + str(self.num_tests_run) + ' Tests run. ' + str(self.overall_errors) + ' Tests failed.\n')
        self.log.write('\n')
        self.log.close()