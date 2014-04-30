import sys
from powerOverEthernet import PowerOverEthernet
from dateTime import DateTime
from smoketest.TestLog import TestLog
from smoketest.mylib.LoginHandler import LoginHandler
from smoketest.mylib.utils import Utils
from smoketest.sysAbout import SystemAbout
from smoketest.sysInfo2 import SystemInformation


def main():
    run_all = RunAll()
    run_all.run_all()


class RunAll():
    def __init__(self):
        self.driver = Utils.create_driver(sys.argv[2])
        # self.testLog = TestLog()

    def run_all(self):
        print('running all tests')
        Utils.delete_existing_logfile()

        login_handler = LoginHandler()
        login_handler.start(self.driver)

        test_log = TestLog('All Tests')
        # testLog.log_it('test')

        sys_info = SystemInformation(login_handler)
        sys_info.run_system_information(self.driver, test_log)

        sys_about = SystemAbout(login_handler)
        sys_about.run_system_about(self.driver, test_log)

        poe = PowerOverEthernet(login_handler)
        poe.run_poe(self.driver, test_log)

        date_time = DateTime(login_handler)
        date_time.run_date_time(self.driver, test_log)

        login_handler.end(self.driver)

if __name__ == "__main__":
    main()