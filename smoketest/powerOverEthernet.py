from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import guiLib

import sys, time, os


def main():
    poe = PowerOverEthernet(True)
    poe.runPoe()


class PowerOverEthernet(object):
    def __init__(self, loggedIn):
        self.loggedIn = loggedIn

    def runPoe(self):
        driver = guiLib.createDriver(sys.argv[2])

        guiLib.loginToRadio(driver, self.loggedIn)

        # driver.switch_to_default_content()
        guiLib.click_element(driver, 'menu_node_7_tree')
        guiLib.click_element(driver, 'menu_node_12')

        print('are we logged in already', self.loggedIn)

        try:
            driver.switch_to_frame("frame_content")
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "PoEConfigWidget1_TW_table")))
            table = driver.find_element_by_id("PoEConfigWidget1_TW_table")

            headers = table.find_elements_by_tag_name('th')
            setHeaders = ['Interface', 'Power Mode', 'Max Milliwatts', 'Status', 'Class']

            count = 0
            for head in headers:
                assert head.text == setHeaders[count], ('Expected ', setHeaders[count], ' but got ', head.text)
                count += 1

            # driver.execute_script("document.getElementById('PoEConfigWidget1_TW_17_description').innerHTML=\"\";")

            interface = table.find_element_by_id("PoEConfigWidget1_TW_17_description").text

            interfaceLen = len(interface)
            assert interfaceLen > 0, ("Expected interface length to be > 0 but was ", interfaceLen)
            time.sleep(2)
        except TimeoutException:
            print("element not found")


if __name__ == "__main__":
    main()