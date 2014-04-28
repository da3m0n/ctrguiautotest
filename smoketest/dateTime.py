from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# import guiLib
import sys
# from smoketest.mylib import IsolatedLoginHandler
from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils
import unittest

def main():
    Utils.delete_existing_logfile()
    date_time = DateTime(IsolatedLoginHandler())
    testLog = TestLog()
    date_time.run_date_time(Utils.create_driver(sys.argv[2]), testLog)
    print("Inside dateTime().main()")


class DateTime(unittest.TestCase):
    def __init__(self, login_manager):
        self.login_manager = login_manager

        # self.test_log = TestLog(self.__class__.__name__)

    def run_date_time(self, driver, testLog):

        gui_lib = Utils()

        self.login_manager.login(driver)

        testLog.start('DateTime')
        testHelper = TestHelper(testLog)

        failure_count = 0

        driver.switch_to_default_content()
        test = driver.find_element_by_id("menu_node_7_tree")

        driver.find_element_by_id("menu_node_7_tree").click()
        gui_lib.click_element(driver, "menu_node_9")
        driver.switch_to_frame("frame_content")

        table = driver.find_element_by_id("DateTimeWidget1_TW_table")
        WebDriverWait(table, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "TableWidget_verticalTableHeading")))

        headers = table.find_elements_by_class_name('TableWidget_verticalTableHeading')
        set_headers = ['Clock Source', 'Date', 'Time', 'Timezone']

        count = 0
        testHelper.assertTrue(len(headers) == 0, 'Expected Headers, got None', 'Testing Headers')

        # for head in headers:
        #     # assert head.text == set_headers[count], ('Expected ', set_headers[count], ' but got ', head.text)
        #     print(set_headers[count], head.text)
        #
        #     if head.text != set_headers[count]:
        #         # self.assertEqual(set_headers[count], head.text, 'test')
        #         # testHelper.assertNotEqual(set_headers[count], head.text)
        #         res = {'expected': set_headers[count], 'detected': head.text}
        #         testLog.log_it(res)
        #         # failure_count += 1
        #     count += 1

        # driver.execute_script("document.getElementById('DateTimeWidget1_TW_1_1').innerHTML=\"\";")
        mycalendar = table.find_element_by_id('DateTimeWidget1_TW_1_1')
        testHelper.assertTrue(len(mycalendar.text) <= 0, 'Expected Calendar length > 0', 'Testing Calendar length')

        driver.execute_script("document.getElementById('DateTimeWidget1_TW_3_1').innerHTML=\"\";")
        timeZone = table.find_element_by_id('DateTimeWidget1_TW_3_1')
        testHelper.assertTrue(len(timeZone.text) <= 0, 'Expected TimeZone length > 0', 'Testing Timezone')

        # testLog.end_log2()
        testLog.end_log(failure_count)
        self.login_manager.logout(driver)
        testLog.close()


if __name__ == "__main__":
    main()