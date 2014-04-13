import sys
from powerOverEthernet import PowerOverEthernet
from dateTime import DateTime
from smoketest.TestLog import TestLog
from smoketest.mylib.LoginHandler import LoginHandler
from smoketest.mylib.utils import Utils


def main():
    run_all = RunAll()
    run_all.run_all()


class RunAll():
    def __init__(self):
        self.driver = Utils.create_driver(sys.argv[2])

    def run_all(self):
        print('running all tests')
        Utils.delete_existing_logfile()

        login_handler = LoginHandler()
        login_handler.start(self.driver)

        testLog = TestLog()

        poe = PowerOverEthernet(login_handler)
        poe.run_poe(self.driver, testLog)

        date_time = DateTime(login_handler)
        date_time.run_date_time(self.driver, testLog)

        login_handler.end(self.driver)

if __name__ == "__main__":
    main()