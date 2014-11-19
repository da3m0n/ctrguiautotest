import sys

import os

import smoketest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from smoketest.aurorasmoketest.mylib.LoginHandler import LoginHandler
from aurorasmoketest.utils import Utils
from aurorasmoketest.AuroraSmokeTest import AuroraSmokeTest
from optparse import OptionParser


def main():
    parser = OptionParser(usage="usage: %prog ipAddress browser")
    # parser.add_option("-c", "--chelp", help="Add arguments for IP Address for radio and target browser")
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("wrong number of arguments")

    run_all = RunAll()
    run_all.do_rest()


class RunAll():
    def do_rest(self):
        driver = Utils.create_driver(sys.argv[2])

        login_handler = LoginHandler(driver)
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


class LoginHandler(object):
    def __init__(self, driver):
        self.utils = Utils(driver)
        self.driver = driver

    def login(self):
        print('doing nothing, already logged from start()')

    def logout(self):
        print('normal logout')

    def start(self):
        self.utils.startBrowser(self.driver)
        self.utils.login(self.driver, 'root', 'admin123')

    def end(self):
        self.driver.switch_to_default_content()
        self.utils.logout(self.driver)


class IsolatedLoginHandler(object):
    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(driver)

    def login(self):
        # self.utils.delete_existing_logfile()
        self.utils.startBrowser(self.driver)
        self.utils.login(self.driver, 'root', 'admin123')

    def logout(self):
        self.driver.switch_to_default_content()
        self.utils.logout(self.driver)

if __name__ == "__main__":
    for i in range(0, 2):
        main()
