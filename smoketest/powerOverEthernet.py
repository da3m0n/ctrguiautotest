from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import guiLib

import sys, time, os
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils
import logging
import pytest


def main():
    Utils.delete_existing_logfile()
    poe = PowerOverEthernet(IsolatedLoginHandler())
    poe.run_poe(Utils.createDriver(sys.argv[2]))


class PowerOverEthernet(object):
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def run_poe(self, driver):

        self.login_manager.login(driver)

        gui_lib = Utils()

        driver.switch_to_default_content()
        gui_lib.click_element(driver, 'menu_node_7_tree')
        gui_lib.click_element(driver, 'menu_node_12')

        errors = open('errors.log', 'a')
        errors.write('======== Power Over Ethernet\n')

        try:
            failure_count = 0
            driver.switch_to_frame("frame_content")
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "PoEConfigWidget1_TW_table")))
            table = driver.find_element_by_id("PoEConfigWidget1_TW_table")

            headers = table.find_elements_by_tag_name('th')
            set_headers = ['Interface', 'Power Mode', 'Max Milliwatts', 'Status', 'Class']

            count = 0
            for head in headers:
                # assert head.text == set_headers[count], ('Expected ', set_headers[count], ' but got ', head.text)
                if head.text != set_headers[count]:
                    errors.write('Expected \"' + set_headers[count] + '\" but got \"' + head.text + '\"\n')
                    failure_count += 1
                count += 1

            # driver.execute_script("document.getElementById('PoEConfigWidget1_TW_19_description').innerHTML=\"\";")

            interface = table.find_element_by_id("PoEConfigWidget1_TW_19_description").text

            interface_len = len(interface)
            # assert interface_len > 0, ("Expected interface length to be > 0 but was ", interface_len)
            if interface_len == 0:
                # failure = "Expected interface length to be > 0 but was " + str(interface_len)
                # print('failed: ', failure)
                errors.write("Expected Interface Length to be > 0 but was " + str(interface_len) + "\n")
                failure_count += 1

            time.sleep(2)
            if failure_count > 0:
                errors.write('======== ' + str(failure_count) + ' failures. End Power Over Ethernet\n\n')
            else:
                errors.write('======== Test Passed')

            errors.close()
            self.login_manager.logout(driver)
        except TimeoutException:
            print("element not found")


if __name__ == "__main__":
    main()