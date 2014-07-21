from enum import Enum
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils
import sys


def main():
    driver = Utils.create_driver(sys.argv[2])
    log_dir = Utils.log_dir()
    test_log = TestLog(PortManager, log_dir)
    # create instance of class here and then  run method of class 
    port_manager = PortManager(IsolatedLoginHandler(driver))
    port_manager.run_port_manager(driver, test_log)
    test_log.close()


class TableHeaders(Enum):
    INDEX = ''
    STATUS = 'Status'
    PORT = 'Port'
    ENABLE = 'Enable'
    DESCRIPTION = 'Description'
    SPEED_DUPLEX = 'Speed - Duplex'
    DEFAULT_USER_PRIORITY = 'Default\nUser Priority'
    MAC_ADDRESS = 'MAC Address'
    MTU = 'MTU'


class PortManager():
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def run_port_manager(self, driver, test_log):
        gui_lib = Utils(driver)
        self.login_manager.login()

        test_log.start('Port Manager')
        test_helper = TestHelper(test_log, driver)

        driver.switch_to_default_content()
        gui_lib.click_element('menu_node_ethernet_tree')
        gui_lib.click_element('menu_node_ethernet')

        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "menu_node_10")))
        driver.switch_to_frame('frame_content')
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'PortSettingsWidget1intSet_TW_table')))
        table = driver.find_element_by_id('PortSettingsWidget1intSet_TW_table')
        headers = table.find_elements_by_tag_name('th')
        headers_list = []
        headers_arr = ['', 'Status1', 'Port', 'Enable', 'Description', 'Speed - Duplex', 'Default\nUser Priority',
                       'MAC Address', 'MTU']

        header_to_hide = [
            "document.getElementById('PortSettingsWidget1intSet_TW_table_header_entity_index').innerHTML=\"\";",
            "document.getElementById('PortSettingsWidget1intSet_TW_table_header_operational_status').innerHTML=\"\";",
            "document.getElementById('PortSettingsWidget1intSet_TW_table_header_port').innerHTML=\"\";",
            "document.getElementById('PortSettingsWidget1intSet_TW_table_header_admin_status').innerHTML=\"\";",
            "document.getElementById('PortSettingsWidget1intSet_TW_table_header_description').innerHTML=\"\";",
            "document.getElementById('PortSettingsWidget1intSet_TW_table_header_user_duplex').innerHTML=\"\";",
            "document.getElementById('PortSettingsWidget1intSet_TW_table_header_priority').innerHTML=\"\";",
            "document.getElementById('PortSettingsWidget1intSet_TW_table_header_mac').innerHTML=\"\";",
            "document.getElementById('PortSettingsWidget1intSet_TW_table_header_mtu').innerHTML=\"\";"]

        # these tests only check that headers are displayed. Wont flag if there are any missing,
        # the order incorrect etc. It is only a all or none deal
        for header in headers:
            headers_list.append(header.text)

        # uncomment to remove headers for testing
        # for header in header_to_hide:
        #     driver.execute_script(header)

        for i in range(len(headers_list)):
            header = headers_list[i]
            header_text_len = len(header)
            test_helper.assert_true(headers[i].text != header,
                                    'Expected ' + header + ' to be > 0 but was ' + str(header_text_len),
                                    'Ensure ' + header + ' visible')

        rows = table.find_elements_by_tag_name('tr')
        test_helper.assert_true(len(rows) <= 0, str(len(rows)) + ' Port Settings rows displayed ',
                                'Ensure Port Settings rows displayed ')

        test_log.close()
        self.login_manager.logout()


if __name__ == '__main__':
    main()
