import sys

import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from smoketest.aurorasmoketest.mylib.LoginHandler import LoginHandler
from utils import Utils
from AuroraSmokeTest import AuroraSmokeTest
from optparse import OptionParser


def main():
    parser = OptionParser(usage="usage: %prog ipAddress browser")
    # parser.add_option("-c", "--chelp", help="Add arguments for IP Address for radio and target browser")
    (options, args) = parser.parse_args()

    if len(args) != 3:
        parser.error("wrong number of arguments")

    run_all = RunAll()
    run_all.do_rest()


class RunAll():
    def do_rest(self):

        driver = Utils.create_driver(sys.argv[3])

        login_handler = LoginHandler(driver, sys.argv[2])
        login_handler.start()
        smoke_test = AuroraSmokeTest(driver)

        try:
            smoke_test.navigate_to_screen('home')
            smoke_test.navigate_to_screen('docs')
            smoke_test.navigate_to_screen('chat')
            smoke_test.navigate_to_screen('share')
            smoke_test.navigate_to_screen('admin')
            
        #     smoke_test.navigate_to_screen('admin/pages')
        #     smoke_test.navigate_to_screen('admin/settings')
        #     smoke_test.navigate_to_screen('admin/data')
        #     smoke_test.navigate_to_screen('admin/stats')
        except Exception as e:
            print(e)
        driver.quit()


class LoginHandler(object):
    def __init__(self, driver, port):
        self.port = port
        self.utils = Utils(driver)
        self.driver = driver

    def start(self):
        self.utils.startBrowser(self.driver, self.port)

    def end(self):
        self.driver.switch_to_default_content()

if __name__ == "__main__":
    counter = 0
    # main()
    while counter < 2:
        try:
            counter += 1
            main()
        except Exception as e:
            import signal

            print("Main loop exception")
            print(e)
            print("About to kill process: ", os.getpid())
            os.kill(os.getpid(), signal.SIGBREAK)
