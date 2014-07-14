from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils
from selenium.webdriver.support import expected_conditions as EC
import sys


def main():
    driver = Utils.create_driver(sys.argv[2])
    log_dir = Utils.log_dir()
    Utils.delete_existing_logfile(log_dir)
    test_log = TestLog(LicenseManagement, log_dir)
    # create instance of class here and then  run method of class 

    test_log.close()


class LicenseManagement():
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def run_license_management(self, driver, test_log):
        gui_lib = Utils(driver)
        self.login_manager.login()

        test_log.start('LicenseManagement')
        test_helper = TestHelper(test_log, driver)

        driver.switch_to_default_content()
        gui_lib.click_element('menu_node_system_tree')
        gui_lib.click_element('menu_node_admin_tree')
        gui_lib.click_element('menu_node_licensing')

        driver.switch_to_frame('frame_content')

        serial_number_label = driver.find_element(By.XPATH, "//body/div/div[1]/fieldset/legend").text
        test_helper.assert_true(len(serial_number_label) <= 0,
                                'Expected ' + serial_number_label + ' to be > 0, but was ' + str(
                                    len(serial_number_label)),
                                'Check ' + serial_number_label + ' visible')

        licensed_features_label = driver.find_element(By.XPATH, "//body/div/div[2]/fieldset/legend").text
        test_helper.assert_true(len(licensed_features_label) <= 0,
                                'Expected ' + licensed_features_label + ' to be > 0, but was ' + str(
                                    len(licensed_features_label)),
                                'Check ' + licensed_features_label + ' visible')

        upload_license_label = driver.find_element(By.XPATH, "//body/div/div[3]/fieldset/legend").text
        test_helper.assert_true(len(upload_license_label) <= 0,
                                'Expected ' + upload_license_label + ' to be > 0, but was ' + str(
                                    len(upload_license_label)),
                                'Check ' + upload_license_label + ' visible')

        sleep(5)
        serial = driver.find_element_by_id('FeatureLicenseWidget1_serial')

        test_helper.assert_true(len(serial.text) <= 0,
                                'Expected serial number to be > 0 but was ' + str(len(serial.text)),
                                'Check Serial Number displayed')

        buttons = driver.find_elements_by_tag_name('button')
        buttons_list = []
        for btn in buttons:
            buttons_list.append(btn.text)

        for i in range(len(buttons_list)):
            button = buttons_list[i]
            button_len = len(button)
            test_helper.assert_true(button_len <= 0,
                                    'Expected ' + button + ' to be > 0 but was ' + str(button_len),
                                    'Ensure ' + button + ' visible')

        test_log.close()
        self.login_manager.logout()


if __name__ == '__main__':
    main()
