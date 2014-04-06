from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import guiLib

import sys, time, os
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils


def main():
    poe = PowerOverEthernet(IsolatedLoginHandler())
    poe.run_poe()


class PowerOverEthernet(object):
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def run_poe(self, driver):
        print('calling power over ethernet')
        # driver = guiLib.createDriver(sys.argv[2])

        self.login_manager.login(driver)
        self.login_manager.logout(driver)

        # guiLib.loginToRadio(driver)

        gui_lib = Utils()

        driver.switch_to_default_content()
        gui_lib.click_element(driver, 'menu_node_7_tree')
        gui_lib.click_element(driver, 'menu_node_12')

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

            # driver.execute_script("document.getElementById('PoEConfigWidget1_TW_17_description').innerHTML=\"\";")

            interface = table.find_element_by_id("PoEConfigWidget1_TW_17_description").text

            interface_len = len(interface)
            assert interface_len > 0, ("Expected interface length to be > 0 but was ", interface_len)
            time.sleep(2)
        except TimeoutException:
            print("element not found")


if __name__ == "__main__":
    main()