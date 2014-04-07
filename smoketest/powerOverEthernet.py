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
    if os.path.isfile('errors.log'):
        os.remove('errors.log')
    else:
        print('No existing error.log file.')

    poe = PowerOverEthernet(IsolatedLoginHandler())
    utils = Utils()
    poe.run_poe(utils.createDriver(sys.argv[2]))


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
        errors.write('________ FAILURES\n')

        try:
            driver.switch_to_frame("frame_content")
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "PoEConfigWidget1_TW_table")))
            table = driver.find_element_by_id("PoEConfigWidget1_TW_table")

            headers = table.find_elements_by_tag_name('th')
            set_headers = ['Interface', 'Power Mode', 'Max Milliwatts', 'Status', 'Class']

            count = 0
            for head in headers:
                assert head.text == set_headers[count], ('Expected ', set_headers[count], ' but got ', head.text)
                count += 1

            driver.execute_script("document.getElementById('PoEConfigWidget1_TW_19_description').innerHTML=\"\";")

            interface = table.find_element_by_id("PoEConfigWidget1_TW_19_description").text

            interface_len = len(interface)
            if interface_len == 0:
                # failure = "Expected interface length to be > 0 but was " + str(interface_len)
                # print('failed: ', failure)
                errors.write("Expected interface length to be > 0 but was " + str(interface_len) + "\n")

            time.sleep(2)
            errors.write('======== End Power Over Ethernet\n\n')

            errors.close()
            self.login_manager.logout(driver)
        except TimeoutException:
            print("element not found")


if __name__ == "__main__":
    main()