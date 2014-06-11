from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sys
from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils
import os

def main():
    log_dir = Utils.log_dir()
    Utils.delete_existing_logfile(log_dir)
    date_time = DateTime(IsolatedLoginHandler())
    test_log = TestLog('Date Time', log_dir)
    date_time.run_date_time(Utils.create_driver(sys.argv[2]), test_log)


class DateTime():
    def __init__(self, login_manager):
        self.login_manager = login_manager
        # self.test_log = TestLog(self.__class__.__name__)

    def run_date_time(self, driver, test_log):

        gui_lib = Utils()

        self.login_manager.login(driver)

        test_log.start('Date Time')
        test_helper = TestHelper(test_log)

        failure_count = 0

        driver.switch_to_default_content()
        gui_lib.click_element(driver, 'menu_node_system_tree')
        gui_lib.click_element(driver, 'menu_node_date_time')

        # gui_lib.click_element(driver, "menu_node_9")
        driver.switch_to_frame("frame_content")

        table = driver.find_element_by_id("DateTimeWidget1_TW_table")
        WebDriverWait(table, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "TableWidget_verticalTableHeading")))

        headers = table.find_elements_by_class_name('TableWidget_verticalTableHeading')

        test_helper.assert_true(len(headers) == 0, 'Expected Headers, got None', 'Testing Headers')

        # driver.execute_script("document.getElementById('DateTimeWidget1_TW_1_1').innerHTML=\"\";")
        mycalendar = table.find_element_by_id('DateTimeWidget1_TW_1_1')
        test_helper.assert_true(len(mycalendar.text) <= 0, 'Expected Calendar length > 0', 'Testing Calendar length')

        driver.execute_script("document.getElementById('DateTimeWidget1_TW_3_1').innerHTML=\"\";")
        time_zone = table.find_element_by_id('DateTimeWidget1_TW_3_1')
        test_helper.assert_true(len(time_zone.text) <= 0, 'Expected TimeZone length > 0', 'Testing Timezone')

        # testLog.end_log2()
        self.login_manager.logout(driver)
        test_log.close()


if __name__ == "__main__":
    main()