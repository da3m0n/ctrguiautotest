import sys
from selenium import webdriver
# from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import time
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.LoginHandler import LoginHandler
from smoketest.mylib.utils import Utils
from smoketest.SmokeTest import SmokeTest, ButtonFinder, TdLabelFinder
from smoketest.SmokeTest import TableColumnHeaderFinder
from smoketest.SmokeTest import TableRowHeaderFinder
from optparse import OptionParser


def main():
    parser = OptionParser(usage="usage: %prog ipAddress browser")
    # parser.add_option("-c", "--chelp", help="Add arguments for IP Address for radio and target browser")
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("wrong number of arguments")

    TEST_TYPE = 'smoketest'
    run_all = RunAll(TEST_TYPE)
    run_all.run_all()

    # Utils.print_tree(Utils.log_dir(), TEST_TYPE)


class RunAll():
    def __init__(self, test_type):
        self.test_type = test_type
        self.dir = Utils.log_dir()
        self.test_log = TestLog(self.dir)
        self.driver = Utils.create_driver(sys.argv[2])
        self.utils = Utils(self.driver, self.test_log)
        print('init')

    def run_all(self):
        self.run_smoke_test()

    def run_smoke_test(self):
        print('Gonna run the smoketests...')
        # driver = Utils.create_driver(sys.argv[2])
        # utils = Utils(driver, self.test_log)

        login_handler = LoginHandler(self.driver)
        login_handler.start()

        test_log = TestLog(self.dir)
        test_helper = TestHelper(test_log, self.driver, self.test_type)

        smoke_test = SmokeTest(self.driver, test_log, test_helper)
        run_smoke_tests(smoke_test)

        login_handler.end()
        test_log.close()


def run_smoke_tests(smoke_test):
    # Start Status Tests

    smoke_test.create_equipment_test('Status/Equipment')
    smoke_test.create_alarms_test('Status/Alarms', ['Clear', 'Expand All', 'Collapse All'], ButtonFinder())
    smoke_test.create('Status/Event Log', ['Type', 'Entity', 'Location', 'Date / Time', 'Message'],
                      TableColumnHeaderFinder(), True)
    smoke_test.create('Status/Sensors', ['Temperature Inlet 1/0', 'Voltage 1/0', 'Current 1/0'],
                      TdLabelFinder())
    smoke_test.create('Status/Reports', ['Helpdesk File:'], TdLabelFinder())

    # # this NOT WORKING as keep getting staleelementException as the page is continually refreshing
    # smoke_test.create('Status/Manufacture Details', ['CID Number:', 'Part Number'], td_label_finder())

    # Start System Configuration Tests
    smoke_test.create('System Configuration/System Information',
                      ['Hardware Version', 'Firmware Version', 'Switch MAC'], TableRowHeaderFinder())
    smoke_test.create('System Configuration/Date & Time', ['Date', 'Time', 'Timezone'], TableRowHeaderFinder())
    smoke_test.create('System Configuration/Connected Devices', ['Local Port', 'Address Type'],
                      TableColumnHeaderFinder())

    # smoke_test.create('System Configuration/PoE Configuration', ['Interface', 'Power Mode', 'Status', 'Class'],
    #                   TableColumnHeaderFinder())
    smoke_test.create('System Configuration/Backup Power', ['Voltage', 'Current', 'Temperature'],
                      TableColumnHeaderFinder())
    # smoke_test.create('System Configuration/Remote Log', ['Address', 'Port'],
    #                   TableColumnHeaderFinder())

    # Start Network Synchronization
    smoke_test.create('Network Sync Configuration/Network Clock',
                      ['Clock Mode (Local PLL)', 'Switchover Mode'],
                      TableRowHeaderFinder())
    smoke_test.create('Network Sync Configuration/Network Sync Sources',
                      ['Port', 'Source State', 'Operational Quality Level Tx', 'Internal Quality Level Rx'],
                      TableRowHeaderFinder())

    # # Start Admin Tests
    smoke_test.create('System Configuration/Admin/Configuration Management', ['Restore From:', 'Config File:'],
                      TdLabelFinder())
    smoke_test.create('System Configuration/Admin/Software Management', ['Active Version:', 'Inactive Version:'],
                      TdLabelFinder())

    # Start Switching & Routing Configuration
    smoke_test.create('Switching & Routing Configuration/Port Manager', ['Port', 'MAC Address'],
                      TableColumnHeaderFinder())
    smoke_test.create('Switching & Routing Configuration/Link Aggregation',
                      ['Group Id', 'Max Capacity', 'Current Capacity'], TableColumnHeaderFinder())
    smoke_test.create('Switching & Routing Configuration/VLAN/VLAN',
                      ['Switch Bridge Mode', 'Transparent VLAN Mode'], TableRowHeaderFinder())
    # smoke_test.create('Switching & Routing Configuration/VLAN/VLAN by Interface',
    # ['Interface', 'Port Mode'], TableColumnHeaderFinder())

    smoke_test.create('Switching & Routing Configuration/Quality of Service/Classification',
                      ['Ingress Priority', 'Pre-Color'], TableColumnHeaderFinder())
    smoke_test.create('Switching & Routing Configuration/Quality of Service/Policing',
                      ['Policy Id', 'Meter Type'], TableColumnHeaderFinder())
    # smoke_test.create('Switching & Routing Configuration/Quality of Service/Scheduling',
    #                   ['Congestion Control'], TableColumnHeaderFinder())

    smoke_test.create('Switching & Routing Configuration/Static Routing', ['Context'],
                      TableColumnHeaderFinder())
    smoke_test.create('Switching & Routing Configuration/OSPF/Routers', ['Router Context', 'OSPF Enable'],
                      TableColumnHeaderFinder())
    smoke_test.create('Switching & Routing Configuration/OSPF/Areas', ['Area', 'Area Type'],
                      TableColumnHeaderFinder())
    # smoke_test.create('Switching & Routing Configuration/OSPF/Interfaces', ['Router Context', 'Interface'],
    #                   TableColumnHeaderFinder())

    # Start Radio Configuration Tests
    smoke_test.create('Radio Configuration/Radio Links',
                      ['Bandwidth', 'Modulation Mode', 'Tx / Rx Spacing'],
                      TableRowHeaderFinder())
    smoke_test.create('Radio Configuration/Radio Link Diagnostics', ['Radio Link', 'RFU Details'],
                      TableRowHeaderFinder())
    smoke_test.create('Radio Configuration/Radio Protection',
                      ['Id', 'Primary Interface', 'Secondary Interface', 'Type'], TableColumnHeaderFinder())
    smoke_test.create('Radio Configuration/Radio Protection Diagnostics',
                      ['Protected Interface', 'Locked Online Plugin', 'Locked Transmit Path'],
                      TableRowHeaderFinder())

    # Start TDM Configuration
    smoke_test.create('TDM Configuration/Pseudowire',
                      ['Switch MAC', 'Mode', 'Recovery Clock Freq'],
                      TableRowHeaderFinder())
    smoke_test.create('TDM Configuration/Tributary Diagnostics',
                      ['Tributary', 'Elapsed Time', 'Severely Errored Seconds'],
                      TableRowHeaderFinder())

    # Start Statistics Tests
    smoke_test.create('Statistics/Interface',
                      ['Interface', 'MTU', 'In Octets', 'Out Octets', 'In Errors'],
                      TableColumnHeaderFinder())
    smoke_test.create('Statistics/Radio Link Performance',
                      ['Active Rx Time', 'Current BER', 'Local RSL', '512QAM Rx Time', 'XPD'],
                      TableRowHeaderFinder())
    smoke_test.create('Statistics/Radio G826',
                      ['Errored Blocks', 'Errored Seconds', 'Background Block Errors'],
                      TableRowHeaderFinder())
    smoke_test.create('Statistics/ARP Cache', ['MAC Address', 'Interface', 'IP Address', 'Mapping'],
                      TableColumnHeaderFinder())
    smoke_test.create('Statistics/MAC Address Table', ['VLAN', 'MAC Address', 'Type', 'PW Index', 'Port'],
                      TableColumnHeaderFinder())


if __name__ == "__main__":

    count = 0
    while 1:

        # time.sleep(5)
        # main()
        try:
            time.sleep(5)
            main()
            count += 1
            print("Run " + str(count) +  " times.")
        except Exception as e:
            import signal
            print("Main loop exception")
            print(e)
            print("About to kill process: ", os.getpid())
            # os.kill(os.getpid(), signal.SIGBREAK)

    # main()