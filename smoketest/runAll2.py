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
from smoketest.SmokeTest import SmokeTest, ButtonFinder, TdLabelFinder, DivTextFinder, SpanTextFinder
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

    Utils.print_tree(Utils.log_dir(), TEST_TYPE)

    # Utils.generate_overall_result(Utils.log_dir(), TEST_TYPE)


from enum import Enum


class ComparisonResult(Enum):
    LATEST = 1
    ACTIVE = 2
    SAME = 3


def reformat_for_compare(swpack):
    # if build is master substitute master for 99.99.99 for easier comparison
    if swpack.find('master') != -1:
        return swpack.replace('master', '99.99.99')
    else:
        return swpack


def must_download_latest(active_swpack, latest_swpack):
    active = active_swpack.split('.')
    decoded_latest = latest_swpack.encode('ascii', 'ignore')
    latest = decoded_latest.split('.')
    res = None

    for i in range(0, min(len(active), len(latest))):
        if compare(int(active[i]), int(latest[i])) == ComparisonResult.SAME or compare(int(active[i]), int(
                latest[i])) == ComparisonResult.ACTIVE:
            res = False
        else:
            res = True
    return res


def compare(active, latest):
    if active < latest:
        return ComparisonResult.LATEST
    elif active > latest:
        return ComparisonResult.ACTIVE
    else:
        return ComparisonResult.SAME


def determine_latest_swpack(active_swpack, latest_swpack):
    active = active_swpack.split('.')
    decoded_latest = latest_swpack.encode('ascii', 'ignore')
    latest = decoded_latest.split('.')

    for i in range(0, min(len(active), len(latest))):
        if compare(int(active[i]), int(latest[i])) == 'same':
            continue
        elif compare(int(active[i]), int(latest[i])) == 'active':
            return 'active'
        else:
            return 'latest'
    return len(active) > len(latest)


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
        # active_sw_version = Utils.get_active_sw_version()
        # latest_swpack = Utils.get_latest_sw_pack_version()
        #
        # # dummies for tests
        # active_sw_version = '3.6.1(41.5629)' #'master.12.1919'
        # latest_swpack = active_sw_version  # 'master.12.1919'
        #
        # swpack = determine_latest_swpack(reformat_for_compare(active_sw_version), reformat_for_compare(latest_swpack))
        # get_latest = must_download_latest(reformat_for_compare(active_sw_version), reformat_for_compare(latest_swpack))
        #
        # if get_latest:
        #     print ('Get latest sw pack...')
        #     Utils.upload_latest(self.run_smoke_test)
        # else:
        #     print ('Using latest, don\'t need to upload latest... ')
        #     self.run_smoke_test()
        #     # self.write_config_test(self.driver)

    @staticmethod
    def get_num_screens(driver):
        num_screens = 0
        side_menu_folders = driver.find_elements_by_xpath("//div[@class='side_menu_tree']")
        for folder in side_menu_folders:
            id_attr = folder.get_attribute('id')
            root_folder = driver.find_element_by_id(id_attr)
            root_folder.click()
            individual_pages = root_folder.find_elements_by_tag_name('a')
            for page in individual_pages:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, page.text)))
                if page.text != '':
                    num_screens += 1
                    # print('page', page.text, num_screens)
        return num_screens

    def run_smoke_test(self):
        print('Gonna run the smoketests...')
        # driver = Utils.create_driver(sys.argv[2])
        # utils = Utils(driver, self.test_log)
        self.utils.delete_existing_dir()

        login_handler = LoginHandler(self.driver)
        login_handler.start()

        test_log = TestLog(self.dir)
        test_helper = TestHelper(test_log, self.driver, self.test_type)

        # Uncomment this to get coverage graph
        # test_log.add_num_screens(RunAll.get_num_screens(self.driver))
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'menu_node_equipment')))
        # self.driver.find_element_by_id('menu_node_equipment').click()

        smoke_test = SmokeTest(self.driver, test_log, test_helper)
        run_smoke_tests(smoke_test)

        login_handler.end()
        test_log.close()


def run_smoke_tests(smoke_test):
    # Start Status Tests

    smoke_test.create_equipment_test('Status/Equipment')
    smoke_test.create_button_test('Status/Alarms', ['Clear', 'Expand All', 'Collapse All'], ButtonFinder())
    smoke_test.create('Status/Event Log', ['Type', 'Date / Time', 'Location2', 'Entity', 'Message'],
                      TableColumnHeaderFinder(), True)
    smoke_test.create('Status/Sensors', ['Temperature Inlet 1/0', 'Voltage 1/0', 'Current 1/0'],
                      DivTextFinder())
    smoke_test.create('Status/Reports', ['Helpdesk File:'], SpanTextFinder())

    # # this NOT WORKING as keep getting staleelementException as the page is continually refreshing
    # smoke_test.create('Status/Manufacture Details', ['CID Number:', 'Part Number'], td_label_finder())

    # Start System Configuration Tests
    print('System Configuration Tests')
    smoke_test.create('System Configuration/System Information',
                      ['Hardware Version2', 'Firmware Version', 'Switch MAC'], TableRowHeaderFinder())
    smoke_test.create('System Configuration/Management IP Address',
                      ['Interface', 'Broadcast Address'], TableColumnHeaderFinder())
    smoke_test.create('System Configuration/Date & Time',
                      ['Date', 'Time', 'Timezone'], TableRowHeaderFinder())
    smoke_test.create('System Configuration/Connected Devices', ['Local Port', 'Address Type'],
                      TableColumnHeaderFinder())
    smoke_test.create('DHCP Relay',
                      ['Enable', 'Discover', 'Request', 'Ack'], TableRowHeaderFinder())
    smoke_test.create('System Configuration/Remote Log', ['Protocol'],
                      TableColumnHeaderFinder())
    smoke_test.create('System Configuration/PoE Configuration', ['Interface', 'Status', 'Class'],
                      TableColumnHeaderFinder())
    smoke_test.create('System Configuration/Backup Power', ['Voltage', 'Current', 'Temperature'],
                      TableColumnHeaderFinder())

    # # Start Admin Tests
    print('admin tests')
    smoke_test.create('System Configuration/Admin/Users', ['Sessionid', 'User', 'Interface'],
                      TableColumnHeaderFinder())
    # TODO Add TACACS+
    smoke_test.create('System Configuration/Admin/Configuration Management', ['Restore From:', 'Config File:'],
                      TdLabelFinder())
    smoke_test.create('System Configuration/Admin/Software Management', ['Active Version:', 'Inactive Version:'],
                      TdLabelFinder())
    smoke_test.create('System Configuration/Admin/License Management', ['Active Version:', 'Inactive Version:'],
                      DivTextFinder())
    smoke_test.create_button_test('System Configuration/Admin/Script Loading', ['Choose File'],
                                  ButtonFinder())
    smoke_test.create('System Configuration/Admin/Strong Security',
                      ['Security Mode'], TableRowHeaderFinder())

    # Start Switching & Routing Configuration
    print('Switching & Routing Configuration tests')
    smoke_test.create('Switching & Routing Configuration/Port Manager', ['Port', 'MAC Address'],
                      TableColumnHeaderFinder())
    smoke_test.create('Switching & Routing Configuration/Interfaces', ['Port Type'],
                      TableColumnHeaderFinder())
    smoke_test.create('Switching & Routing Configuration/Static Routing', ['Context', 'Prefix', 'Next Hop'],
                      TableColumnHeaderFinder())
    smoke_test.create('Switching & Routing Configuration/Link Aggregation',
                      ['Group Id', 'Max Capacity', 'Current Capacity'], TableColumnHeaderFinder())
    smoke_test.create('Switching & Routing Configuration/VLAN/VLAN',
                      ['Switch Bridge Mode', 'Transparent VLAN Mode'], TableRowHeaderFinder())
    smoke_test.create('Switching & Routing Configuration/VLAN/VLAN by Interface',
                      ['Interface', 'Port Mode'], TableColumnHeaderFinder())
    smoke_test.create('Switching & Routing Configuration/VLAN/C-VLAN to S-VLAN Mapping',
                     ['Interface', 'Port Mode'], TableColumnHeaderFinder())

    smoke_test.create('Switching & Routing Configuration/Quality of Service/Classification',
                      ['Ingress Priority', 'Pre-Color'], TableColumnHeaderFinder())
    smoke_test.create('Switching & Routing Configuration/Quality of Service/Policing',
                      ['Policy Id', 'Meter Type'], TableColumnHeaderFinder())
    # TODO FIX THIS smoke_test.create('Switching & Routing Configuration/Quality of Service/Scheduling',
    #                   ['Internal Weight'], TableColumnHeaderFinder())

    smoke_test.create('Switching & Routing Configuration/OSPF/Routers',
                      ['Router Context', 'Router Id'],
                      TableColumnHeaderFinder())
    smoke_test.create('Switching & Routing Configuration/OSPF/Areas',
                      ['Area', 'Area Type'],
                      TableColumnHeaderFinder())
    # TODO FIX - GOING TO WRONG PAGE smoke_test.create('Switching & Routing Configuration/OSPF/Interfaces',
    #                   ['Router Context', 'Interface'],
    #                   TableColumnHeaderFinder())


    # Start Radio Configuration Tests
    print('Radio Configuration Tests')
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


    # Start Network Synchronization
    print('Network Synchronization Tests')
    smoke_test.create('Network Sync Configuration/Network Clock',
                     ['Clock Mode (Local PLL)', 'Switchover Mode'],
                     TableRowHeaderFinder())
    smoke_test.create('Network Sync Configuration/Network Sync Sources',
                      ['Port', 'Source State'],
                      TableColumnHeaderFinder())
    smoke_test.create('Network Sync Configuration/Interface Synchronization',
                      ['Port', 'Source State'],
                      TableRowHeaderFinder())


    # Start TDM Configuration
    print('TDM Configuration Tests')
    smoke_test.create('TDM Configuration/Pseudowire',
                      ['Switch MAC', 'Mode', 'Recovery Clock Freq'],
                      TableRowHeaderFinder())
    smoke_test.create('TDM Configuration/Tributary Diagnostics',
                      ['Tributary', 'Elapsed Time', 'Severely Errored Seconds'],
                      TableRowHeaderFinder())

    # Start Statistics Tests
    print('Statistics Tests')
    smoke_test.create('Statistics/Interface Counters',
                      ['Interface', 'MTU', 'In Octets', 'Out Octets', 'In Errors'],
                      TableColumnHeaderFinder())
    smoke_test.create('Statistics/Radio Link Performance',
                      ['Active Rx Time', 'Current BER', 'Local RSL', '512QAM Rx Time', 'XPD'],
                      TableRowHeaderFinder())
    smoke_test.create('Statistics/Radio G.826',
                      ['Errored Blocks', 'Errored Seconds', 'Background Block Errors'],
                      TableRowHeaderFinder())
    smoke_test.create('Statistics/ARP Cache',
                      ['MAC Address', 'Interface', 'IP Address', 'Mapping'],
                      TableColumnHeaderFinder())
    smoke_test.create('Statistics/MAC Address Table',
                      ['VLAN', 'MAC Address', 'Type', 'PW Index', 'Port'],
                      TableColumnHeaderFinder())


if __name__ == "__main__":

    count = 0
    # while 1:
    for x in xrange(1):
        # time.sleep(5)
        # main()
        try:
            time.sleep(5)
            main()
            count += 1
            print("Run " + str(count) + " times.")
        except Exception as e:
            import signal
            print("Main loop exception")
            print(e)
            print("About to kill process: ", os.getpid())
            # os.kill(os.getpid(), signal.SIGBREAK)

    # main()