import sys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smoketest.admin.configManagement import ConfigManagement
from smoketest.admin.license_management import LicenseManagement
from smoketest.admin.software_management import SoftwareManagement
from smoketest.status.alarms import Alarms
from smoketest.status.eventLog import EventLog
from smoketest.status.sensors import Sensors
from smoketest.systemconfiguration.dateTime import DateTime
from smoketest.TestLog import TestLog
from smoketest.systemconfiguration.manufactureDetails import ManufactureDetails
from smoketest.mylib.LoginHandler import LoginHandler
from smoketest.mylib.utils import Utils
from smoketest.systemconfiguration.powerOverEthernet import PowerOverEthernet
from smoketest.systemconfiguration.sysAbout import SystemAbout
from smoketest.systemconfiguration.sysInfo import SystemInformation
from smoketest.systemconfiguration.EquipmentView import EquipmentView
from smoketest.ethernetconfiguration.portManager import PortManager
from smoketest.tdmconfiguration.pseudowire import PseudoWire
from smoketest.SmokeTest import SmokeTest, label_and_value_finder
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
        active_sw_version = Utils.get_active_sw_version()
        latest_swpack = Utils.get_latest_sw_pack_version()

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
        utils = Utils(driver)
        utils.delete_existing_dir()

        # driver.Chrome("C:\ChromeDriver\chromedriver.exe")
        # driver.Firefox()
        # driver.Ie()

        login_handler = LoginHandler(driver)
        login_handler.start()

        test_log = TestLog('All Tests', self.dir)

        # test_log.add_num_screens(self.get_num_screens(driver))
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'menu_node_equipment')))
        # driver.find_element_by_id('menu_node_equipment').click()

        smoke_test = SmokeTest(driver, test_log)

        # smoke_test.create('System Configuration/System Information',
        #                   ['Hardware Version', 'Firmware Version', 'Switch MAC'], table_row_header_finder())
        # smoke_test.create('System Configuration/Date & Time',
        #                   ['Date', 'Time', 'Timezone'], table_row_header_finder())
        # smoke_test.create('System Configuration/PoE Configuration', ['Interface', 'Status', 'Class'],
        #                   table_column_header_finder())
        # smoke_test.create('Statistics/Radio Link Performance',
        #                   ['Active Rx Time', 'Current BER', 'Local RSL', '512QAM Rx Time', 'XPD'],
        #                   table_row_header_finder())
        # smoke_test.create('Radio Configuration/Radio Link Diagnostics', ['Radio Link', 'RFU Details'],
        #                   table_row_header_finder())
        # smoke_test.create('Radio Configuration/Radio Link Protection',
        #                   ['Id', 'Primary Interface', 'Secondary Interface', 'Type'], table_column_header_finder())
        # smoke_test.create('Radio Configuration/Radio Protection Diagnostics',
        #                   ['Prot Interface', 'Locked Online Plugin', 'Locked Transmit Path'], table_column_header_finder())
        # smoke_test.create('TDM Configuration/Tributary Diagnostics',
        #                   ['Tributary', 'Elapsed Time', 'Severely Errored Seconds'],
        #                   table_row_header_finder())

        smoke_test.create('System Configuration/Admin/Software Management',
                          ['Active Version', 'Inactive Version', 'Status'],
                          label_and_value_finder())


        # smoke_test.create('Statistics/ARP Cache', ['MAC Address', 'Interface', 'IP Address', 'Media Type'],
        #                   column_header_finder())
        # smoke_test.create('Statistics/Ethernet',
        #                   ['Interface', 'FCS Errors', 'Late Collisions', 'Symbol Errors'],
        #                   column_header_finder())

        # equipment_view = EquipmentView(login_handler)
        # equipment_view.run_equipment_view(driver, test_log)
        #
        # sys_about = SystemAbout(login_handler)
        # sys_about.run_system_about(driver, test_log)
        #
        # manu_details = ManufactureDetails(login_handler)
        # manu_details.run_manufacture_details(driver, test_log)
        #
        # sys_info = SystemInformation(login_handler)
        # sys_info.run_system_information(driver, test_log)
        #
        # date_time = DateTime(login_handler)
        # date_time.run_date_time(driver, test_log)
        #
        # poe = PowerOverEthernet(login_handler)
        # poe.run_poe(driver, test_log)
        #
        # sensors = Sensors(login_handler)
        # sensors.run_sensors(driver, test_log)
        #
        # event_log = EventLog(login_handler)
        # event_log.run_event_log(driver, test_log)
        #
        # # # restart this test when id's have been added to Alarms page
        # # # alarms = Alarms(login_handler)
        # # # alarms.run_alarms(driver, test_log)
        #
        # config_management = ConfigManagement(login_handler)
        # config_management.run_config_management(driver, test_log)
        #
        # software_management = SoftwareManagement(login_handler)
        # software_management.run_software_management(driver, test_log)
        #
        # license_management = LicenseManagement(login_handler)
        # license_management.run_license_management(driver, test_log)
        #
        # port_manager = PortManager(login_handler)
        # port_manager.run_port_manager(driver, test_log)
        #
        # pseudo_wire = PseudoWire(login_handler)
        # pseudo_wire.run_pseudo_wire(driver, test_log)

        login_handler.end()
        test_log.close()


if __name__ == "__main__":
    main()