import sys
from selenium import webdriver
# from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import time
import os
from smoketest.TestHelper import TestHelper

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smoketest.TestLog import TestLog
from smoketest.mylib.LoginHandler import LoginHandler
from smoketest.mylib.utils import Utils
from optparse import OptionParser


def main():
    parser = OptionParser(usage="usage: %prog ipAddress browser")
    # parser.add_option("-c", "--chelp", help="Add arguments for IP Address for radio and target browser")
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("wrong number of arguments")

    TEST_TYPE = "writeConfigTest"

    run_all = RunAll(TEST_TYPE)
    run_all.run_all()

    Utils.print_tree(Utils.log_dir(), TEST_TYPE)


class RunAll():
    def __init__(self, test_type):
        self.dir = Utils.log_dir()
        self.test_log = TestLog(self.dir, test_type)
        self.driver = Utils.create_driver(sys.argv[2])
        self.utils = Utils(self.driver, self.test_log)
        self.test_type = test_type
        print('init')

    def run_all(self):
        self.utils.delete_existing_dir()

        login_handler = LoginHandler(self.driver)
        login_handler.start()

        self.write_config_test(self.driver)

        # test_log = TestLog(self.dir)
        # test_helper = TestHelper(self.test_log, self.driver)

        login_handler.end()
        # self.test_log.close()

    def write_config_test(self, driver):
        # test_log = TestLog(self.dir)
        test_helper = TestHelper(self.test_log, driver, self.test_type)

        self.utils.navigate_to_screen("System Configuration/System Information")
        driver.switch_to_default_content()

        # driver.switch_to_frame("frame_content")
        time.sleep(5)
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "SystemInformationWidget1_TW_3_1_renderer")))

        node_name = driver.find_element_by_id("SystemInformationWidget1_TW_3_1_renderer_input")
        contact = driver.find_element_by_id("SystemInformationWidget1_TW_5_1_renderer_input")
        location = driver.find_element_by_id("SystemInformationWidget1_TW_6_1_renderer_input")

        node_name.clear()
        contact.clear()
        location.clear()

        node_name.send_keys(self.random_letters(10))
        contact.send_keys(self.random_letters(30))
        location.send_keys(self.random_letters(30))

        initial_node_name = node_name.get_attribute("value")
        initial_contact = contact.get_attribute("value")
        initial_location = location.get_attribute("value")

        apply_btn = driver.find_element_by_class_name("apply")
        apply_btn.is_enabled()
        apply_btn.click()

        # self.utils.navigate_to_screen("System Configuration/System Information")
        print('about to press refresh')
        ActionChains(driver).key_down(Keys.F5).perform()
        print('refresh pressed after this point')

        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, "SystemInformationWidget1_TW_3_1_renderer")))

        updated_node_name = driver.find_element_by_id("SystemInformationWidget1_TW_3_1_renderer_input").get_attribute(
            "value")
        updated_contact = driver.find_element_by_id("SystemInformationWidget1_TW_5_1_renderer_input").get_attribute(
            "value")
        updated_location = driver.find_element_by_id("SystemInformationWidget1_TW_6_1_renderer_input").get_attribute(
            "value")

        print(initial_node_name, updated_node_name)
        print(initial_contact, updated_contact)
        print(initial_location, updated_location)

        v1 = self.compare_vals(initial_node_name, updated_node_name)
        v2 = self.compare_vals(initial_contact, updated_contact)
        v3 = self.compare_vals(initial_location, updated_location)

        # test_helper.assert_true(initial_node_name != updated_node_name,
        #                         'Expected ' + initial_node_name + ' but was ' + updated_node_name,
        #                         'Ensure Node name is persisted')
        test_helper.assert_true(False,
                                'Expected this but was that',
                                'Ensure Node name is persisted')
        print(v1, v2, v3)
        self.test_log.close()


    def compare_vals(self, initial_node_name, updated_node_name):
        return initial_node_name == updated_node_name


    import string


    def random_letters(self, size=6, chars=string.ascii_letters + string.digits):
        import random

        return ''.join(random.choice(chars) for _ in range(size))



if __name__ == "__main__":
    main()