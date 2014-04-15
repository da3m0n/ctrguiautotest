from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import guiLib

import sys, time, os
from smoketest.TestLog import TestLog
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils
import logging
import pytest
import pickle
import timeit


def main():
    Utils.delete_existing_logfile()
    poe = PowerOverEthernet(IsolatedLoginHandler())
    testLog = TestLog()
    poe.run_poe(Utils.create_driver(sys.argv[2]), testLog)


class PowerOverEthernet(object):
    def __init__(self, login_manager):
        self.login_manager = login_manager
        # self.test_log = TestLog(self.__class__.__name__)

    def run_poe(self, driver, testLog):
        self.login_manager.login(driver)

        gui_lib = Utils()

        driver.switch_to_default_content()
        gui_lib.click_element(driver, 'menu_node_7_tree')
        gui_lib.click_element(driver, 'menu_node_12')

        testLog.start('PowerOverEthernet')

        # gui_lib.find_element_by_id(driver, "PoEConfigWidget1_TW_table1")

        failure_count = 0
        driver.switch_to_frame("frame_content")
        table_element = "PoEConfigWidget1_TW_table"
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, table_element)))
        table = driver.find_element_by_id(table_element)

        headers = table.find_elements_by_tag_name('th')
        set_headers = ['Interface', 'Power Mode', 'Max Milliwatts', 'Status', 'Class']

        count = 0
        for head in headers:
            if head.text != set_headers[count]:
                testLog.log_it('Expected \"' + set_headers[count] + '\" but got \"' + head.text + '\"')
                res = {'expected': set_headers[count], 'detected': head.text}
                testLog.log_it(res)
                failure_count += 1
            count += 1

        # insert error to test. Uncomment when needed
        driver.execute_script("document.getElementById('PoEConfigWidget1_TW_19_description').innerHTML=\"\";")

        interface = table.find_element_by_id("PoEConfigWidget1_TW_19_description").text

        interface_len = len(interface)
        if interface_len == 0:
            res = {'expected': '> 0', 'detected': str(interface_len)}
            testLog.log_it(res)
            # testLog.log_it("Expected Interface Length to be > 0 but was " + str(interface_len) + "\n")
            failure_count += 1

        time.sleep(2)

        testLog.end_log(failure_count)

        self.login_manager.logout(driver)

        testLog.close()


if __name__ == "__main__":
    main()