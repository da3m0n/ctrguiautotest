from time import sleep
from selenium.webdriver.common.by import By
from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils
import sys


def main():
    print('main')
    log_dir = Utils.log_dir()
    sensors = Sensors(IsolatedLoginHandler())
    test_log = TestLog('Sensors', log_dir)
    sensors.run_sensors(Utils.create_driver(sys.argv[2]), test_log)
    test_log.close()


class Sensors():
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def run_sensors(self, driver, test_log):
        gui_lib = Utils(driver)
        self.login_manager.login()

        test_log.start('Sensors')
        test_helper = TestHelper(test_log, driver)

        driver.switch_to_default_content()
        gui_lib.click_element('menu_node_sensors')

        driver.switch_to_frame('frame_content')

        title = driver.find_element(By.XPATH, "//body/fieldset/legend").text
        test_helper.assert_true(len(title) == 0, 'Expected page title, got None', 'Test page title is displayed')

        table = gui_lib.find_element_by_id(driver, 'tableWidget1_table')
        # find the table header as a delay
        gui_lib.find_element_by_id(driver, 'tableWidget1_table_header')

        table_rows = table.find_elements_by_tag_name('tr')
        print('table_rows', table_rows)
        self.login_manager.logout()


if __name__ == '__main__':
    main()
