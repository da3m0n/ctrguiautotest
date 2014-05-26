import sys
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils


def main():
    Utils.delete_existing_logfile()
    poe = PowerOverEthernet(IsolatedLoginHandler())
    test_log = TestLog('Power Over Ethernet')
    poe.run_poe(Utils.create_driver(sys.argv[2]), test_log)


class PowerOverEthernet(object):
    def __init__(self, login_manager):
        self.login_manager = login_manager
        # self.test_log = TestLog(self.__class__.__name__)

    def run_poe(self, driver, test_log):
        self.login_manager.login(driver)

        gui_lib = Utils()
        test_helper = TestHelper(test_log)

        driver.switch_to_default_content()
        gui_lib.click_element(driver, 'menu_node_7_tree')
        gui_lib.click_element(driver, 'menu_node_12')

        test_log.start('Power Over Ethernet')

        # gui_lib.find_element_by_id(driver, "PoEConfigWidget1_TW_table1")

        failure_count = 0
        driver.switch_to_frame("frame_content")
        table_element = "PoEConfigWidget1_TW_table"
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, table_element)))
        table = driver.find_element_by_id(table_element)

        headers = table.find_elements_by_tag_name('th')

        test_helper.assert_true(len(headers) > 0, 'Expected Headers, got None', 'Testing Headers')

        # insert error to test. Uncomment when needed
        driver.execute_script("document.getElementById('PoEConfigWidget1_TW_13_description').innerHTML=\"\";")

        interface = table.find_element_by_id("PoEConfigWidget1_TW_13_description").text

        interface_len = len(interface)
        test_helper.assert_true(len(interface) <= 0, 'Expected Interface length > 0', 'Testing Interfaces')

        time.sleep(2)

        self.login_manager.logout(driver)
        test_log.close()

if __name__ == "__main__":
    main()