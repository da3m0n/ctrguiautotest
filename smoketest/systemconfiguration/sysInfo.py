import sys, os
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.utils import Utils
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler


def main():
    log_dir = Utils.log_dir()
    system_info = SystemInformation(IsolatedLoginHandler())
    test_log = TestLog('System Information', log_dir)
    system_info.run_system_information(Utils.create_driver(sys.argv[2]), test_log)
    test_log.close()


class SystemInformation(object):
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def run_system_information(self, driver, test_log):
        gui_lib = Utils(driver)

        self.login_manager.login()

        usr = "root"
        pw = "admin123"
        timetup = time.localtime()
        iso = time.strftime('%Y-%m-%d %H:%M:%S ', timetup)
        print "=====", iso, "====="

        test_log.start('System Information')
        test_helper = TestHelper(test_log, driver)

        driver.switch_to_default_content()

        gui_lib.click_element('menu_node_system_tree')
        gui_lib.click_element('menu_node_system_info')

        driver.switch_to_frame("frame_content")
        table = driver.find_element_by_id("SystemInformationWidget1_TW_table")
        WebDriverWait(table, 10).until(EC.presence_of_element_located((By.ID, "SystemInformationWidget1_TW_0")))

        headers = table.find_elements_by_tag_name('th')
        test_helper.assert_true(len(headers) == 0, 'Expected Headers, got None', 'Testing Headers')

        # hwVersion = table.find_element_by_id('SystemInformationWidget1_TW_0_1')
        # driver.execute_script("document.getElementById('SystemInformationWidget1_TW_0_1_renderer').innerHTML=\"\";")
        # hwVersionLen = len(hwVersion.text)
        # testHelper.assertTrue(len(hwVersion.text) > 0, 'Expected Headers, got None', 'Testing Headers')

        # assert hwVersionLen > 0, ('Expected length of Hardware Version to be greater than zero but was ', hwVersionLen)

        sw_version = table.find_element_by_id('SystemInformationWidget1_TW_1_1')
        # driver.execute_script("document.getElementById('SystemInformationWidget1_TW_1_1').innerHTML=\"\";")
        test_helper.assert_true(len(sw_version.text) == 0, 'Expected SW Version to be > 0',
                                'Testing SW Version Length')
        # assert swVersionLen > 0, ('Expected length of Software Version to be greater than zero but was ', swVersionLen)

        # firmVersion = table.find_element_by_id('SystemInformationWidget1_TW_2_1')
        # firmVersionLen = len(firmVersion.text)
        # assert firmVersionLen > 0, ('Expected length of Firmware Version to be greater than zero but was ', firmVersionLen)

        time.sleep(2)
        self.login_manager.logout()


if __name__ == "__main__":
    main()
