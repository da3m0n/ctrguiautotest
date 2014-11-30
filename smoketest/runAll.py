import sys
from time import sleep
from selenium import webdriver
# from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smoketest.TestLog import TestLog
from smoketest.mylib.LoginHandler import LoginHandler
from smoketest.mylib.utils import Utils
from smoketest.SmokeTest import SmokeTest, td_label_finder, button_finder
from smoketest.SmokeTest import table_column_header_finder
from smoketest.SmokeTest import table_row_header_finder
from optparse import OptionParser


def main():
    parser = OptionParser(usage="usage: %prog ipAddress browser")
    # parser.add_option("-c", "--chelp", help="Add arguments for IP Address for radio and target browser")
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("wrong number of arguments")

    run_all = RunAll()
    run_all.run_all()

    Utils.print_tree(Utils.log_dir())


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
    def __init__(self):
        self.dir = Utils.log_dir()
        self.test_log = TestLog('All Tests', self.dir)
        print('init')

    def run_all(self):
        # active_sw_version = Utils.get_active_sw_version()
        # latest_swpack = Utils.get_latest_sw_pack_version()

        # dummies for tests
        active_sw_version = 'master.12.1919'
        latest_swpack = 'master.12.1919'

        # swpack = determine_latest_swpack(reformat_for_compare(active_sw_version), reformat_for_compare(latest_swpack))
        get_latest = must_download_latest(reformat_for_compare(active_sw_version), reformat_for_compare(latest_swpack))

        if get_latest:
            print ('Get latest sw pack...')
            Utils.upload_latest(self.do_rest)
        else:
            print ('Using latest, don\'t need to upload latest... ')
            self.do_rest()

    def get_num_screens(self, driver):
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

    def do_rest(self):
        print('Gonna run the smoketests...')
        driver = Utils.create_driver(sys.argv[2])
        utils = Utils(driver, self.test_log)
        utils.delete_existing_dir()

        # driver.Chrome("C:\ChromeDriver\chromedriver.exe")
        # driver.Firefox()
        # driver.Ie()

        login_handler = LoginHandler(driver)
        login_handler.start()

        test_log = TestLog('All Tests', self.dir)

        # Uncomment this to get coverage graph
        test_log.add_num_screens(self.get_num_screens(driver))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'menu_node_equipment')))
        driver.find_element_by_id('menu_node_equipment').click()

        smoke_test = SmokeTest(driver, test_log)

        # Start Status Tests
        smoke_test.create_equipment_test('Status/Equipment')
        smoke_test.create_alarms_test('Status/Alarms', ['Clear', 'Expand All', 'Collapse All'], button_finder())
        smoke_test.create('Status/Event Log', ['Type', 'Entity', 'Location', 'Date / Time', 'Message'],
                          table_column_header_finder(), True)
        smoke_test.create('Status/Sensors', ['Temperature Inlet 1/0', 'Voltage 1/0', 'Current 1/0'],
                          td_label_finder())
        smoke_test.create('Status/Reports', ['Helpdesk File:'], td_label_finder())

        # this NOT WORKING as keep getting staleelementException as the page is continually refreshing
        # smoke_test.create('Status/Manufacture Details', ['CID Number:', 'Part Number'], td_label_finder())

        # Start System Configuration Tests
        smoke_test.create('System Configuration/System Information',
                          ['Hardware Version', 'Firmware Version', 'Switch MAC'], table_row_header_finder())
        smoke_test.create('System Configuration/Date & Time',
                          ['Date', 'Time', 'Timezone'], table_row_header_finder())
        smoke_test.create('System Configuration/PoE Configuration', ['Interface', 'Power Mode', 'Status', 'Class'],
                          table_column_header_finder())
        smoke_test.create('System Configuration/Backup Power', ['Voltage', 'Current', 'Temperature'],
                          table_column_header_finder())

        # Start Network Synchronization
        smoke_test.create('System Configuration/Network Synchronization/Network Clock',
                          ['Clock Mode (Local PPL)', 'Switchover Mode'],
                          table_row_header_finder())

        # Start Admin Tests
        smoke_test.create('System Configuration/Admin/Configuration Management', ['Restore From:', 'Config File:'],
                          td_label_finder())
        smoke_test.create('System Configuration/Admin/Software Management', ['Active Version:', 'Inactive Version:'],
                          td_label_finder())

        # Start Ethernet Configuration
        smoke_test.create('Ethernet Configuration/Port Manager', ['Port', 'MAC Address'], table_column_header_finder())

        # Start Radio Configuration Tests
        smoke_test.create('Radio Configuration/Radio Links',
                          ['Bandwidth:', 'Modulation Mode:', 'Tx / Rx Spacing:'],
                          td_label_finder())
        smoke_test.create('Radio Configuration/Radio Link Diagnostics', ['Radio Link', 'RFU Details'],
                          table_row_header_finder())
        smoke_test.create('Radio Configuration/Radio Protection',
                          ['Id', 'Primary Interface', 'Secondary Interface', 'Type'], table_column_header_finder())
        smoke_test.create('Radio Configuration/Radio Protection Diagnostics',
                          ['Protected Interface', 'Locked Online Plugin', 'Locked Transmit Path'],
                          table_row_header_finder())

        # Start TDM Configuration
        smoke_test.create('TDM Configuration/Tributary Diagnostics',
                          ['Tributary', 'Elapsed Time', 'Severely Errored Seconds'],
                          table_row_header_finder())
        smoke_test.create('TDM Configuration/Pseudowire',
                          ['Switch MAC', 'Mode', 'Recovery Clock Freq'],
                          table_row_header_finder())

        # Start Statistics Tests
        smoke_test.create('Statistics/Interface',
                          ['Interface', 'MTU', 'In Octets', 'Out Octets', 'In Errors'],
                          table_column_header_finder())
        smoke_test.create('Statistics/Radio Link Performance',
                          ['Active Rx Time', 'Current BER', 'Local RSL', '512QAM Rx Time', 'XPD'],
                          table_row_header_finder())
        smoke_test.create('Statistics/Ethernet',
                          ['Interface', 'FCS Errors', 'Late Collisions', 'Symbol Errors'],
                          table_column_header_finder())
        smoke_test.create('Statistics/ARP Cache', ['MAC Address', 'Interface', 'IP Address', 'Mapping'],
                          table_column_header_finder())
        smoke_test.create('Statistics/MAC Address Table', ['VLAN', 'MAC Address', 'Type', 'PW Index', 'Port'],
                          table_column_header_finder())

        login_handler.end()
        test_log.close()


if __name__ == "__main__":
    main()