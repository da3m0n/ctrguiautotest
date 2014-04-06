import sys
from powerOverEthernet import PowerOverEthernet
from dateTime import DateTime
from smoketest.mylib.LoginHandler import LoginHandler


# def runAll():
#     login_handler = LoginHandler()
#     login_handler.start()
#
#     poe = PowerOverEthernet(login_handler)
#     poe.runPoe()
#
#     date_time = DateTime(login_handler)
#     date_time.run_date_time()
#
#     login_handler.end()
from smoketest.mylib.utils import Utils


def main():
    run_all = RunAll()
    run_all.run_all()


class RunAll():
    def __init__(self):
        print('Run all')
        self.utils = Utils()
        self.driver = self.utils.createDriver(sys.argv[2])

    def run_all(self):
        print('running all tests')
        login_handler = LoginHandler()
        # driver = self.utils.createDriver(sys.argv[2])
        login_handler.start(self.driver)

        poe = PowerOverEthernet(login_handler)
        poe.run_poe(self.driver)

        date_time = DateTime(login_handler)
        date_time.run_date_time(self.driver)

        login_handler.end(self.driver)

if __name__ == "__main__":
    main()

    # runAll()
