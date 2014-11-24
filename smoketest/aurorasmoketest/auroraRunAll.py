import sys

import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from smoketest.aurorasmoketest.mylib.LoginHandler import LoginHandler
from aurorasmoketest.utils import Utils
from AuroraSmokeTest import AuroraSmokeTest
from optparse import OptionParser


def main(counter):
    parser = OptionParser(usage="usage: %prog ipAddress browser")
    # parser.add_option("-c", "--chelp", help="Add arguments for IP Address for radio and target browser")
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("wrong number of arguments")

    run_all = RunAll()
    run_all.do_rest(counter)


class RunAll():
    def do_rest(self, counter):
        driver = Utils.create_driver(sys.argv[2])
        try:
            login_handler = LoginHandler(driver, counter)
            login_handler.start()
            smoke_test = AuroraSmokeTest(driver)

            # Start Status Tests
            smoke_test.navigate_to_screen('Status/Equipment')
            smoke_test.navigate_to_screen('Status/Alarms')
            smoke_test.navigate_to_screen('Status/Event Log')
            smoke_test.navigate_to_screen('Status/Sensors')
            smoke_test.navigate_to_screen('Status/Reports')
            smoke_test.navigate_to_screen('Status/Manufacture Details')

            smoke_test.navigate_to_screen('System Configuration/System Information')
            smoke_test.navigate_to_screen('System Configuration/Date & Time')
            smoke_test.navigate_to_screen('System Configuration/Connected Devices')
            smoke_test.navigate_to_screen('System Configuration/PoE Configuration')
            smoke_test.navigate_to_screen('System Configuration/Backup Power')

            # # Start Network Synchronization
            smoke_test.navigate_to_screen('System Configuration/Network Synchronization/Network Clock')
            smoke_test.navigate_to_screen('System Configuration/Network Synchronization/Network Sync Sources')

            # # Start Admin Tests
            smoke_test.navigate_to_screen('System Configuration/Admin/Configuration Management')
            smoke_test.navigate_to_screen('System Configuration/Admin/Software Management')
            smoke_test.navigate_to_screen('System Configuration/Admin/License Management')

            # # Start Ethernet Configuration
            smoke_test.navigate_to_screen('Ethernet Configuration/Port Manager')
            # No license for LA
            # smoke_test.navigate_to_screen('Ethernet Configuration/Link Aggregation')

            # # Start Radio Configuration Tests
            smoke_test.navigate_to_screen('Radio Configuration/Radio Links')
            smoke_test.navigate_to_screen('Radio Configuration/Radio Link Diagnostics')
            smoke_test.navigate_to_screen('Radio Configuration/Radio Protection')
            smoke_test.navigate_to_screen('Radio Configuration/Radio Protection Diagnostics')

            # # Start TDM Configuration
            smoke_test.navigate_to_screen('TDM Configuration/Pseudowire')
            smoke_test.navigate_to_screen('TDM Configuration/Tributary Diagnostics')

            # # Start Statistics Tests
            smoke_test.navigate_to_screen('Statistics/Interface')
            smoke_test.navigate_to_screen('Statistics/Ethernet')
            smoke_test.navigate_to_screen('Statistics/Radio Link Performance')
            # Need to handle pop up
            # smoke_test.navigate_to_screen('Statistics/Radio Link History')
            smoke_test.navigate_to_screen('Statistics/Radio G826')
            smoke_test.navigate_to_screen('Statistics/ARP Cache')
            smoke_test.navigate_to_screen('Statistics/MAC Address Table')

            login_handler.end()
        except Exception, e:
            print(e)
            driver.get("http://" + sys.argv[1] + "/logout")
            driver.quit()


class LoginHandler(object):
    def __init__(self, driver, counter):
        self.utils = Utils(driver)
        self.driver = driver
        self.counter = counter

    def login(self):
        print('doing nothing, already logged from start()')

    def logout(self):
        print('normal logout')

    def start(self):
        self.utils.startBrowser(self.driver)
        self.utils.login(self.driver, 'root', 'admin123', counter)

    def end(self):
        self.driver.switch_to_default_content()
        self.utils.logout(self.driver)


if __name__ == "__main__":
    counter = 0
    while 1:
        try:
            counter += 1
            main(counter)
        except Exception, e:
            import signal
            print("Main loop exception")
            print(e)
            print("About to kill process: ", os.getpid())
            os.kill(os.getpid(), signal.SIGBREAK)
