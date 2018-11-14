import sys
import traceback

from selenium import webdriver
# from selenium.webdriver.chrome import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import time
import os
import os.path, time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.LoginHandler import LoginHandler
from smoketest.mylib.utils import Utils, GlobalFuncs
from smoketest.SmokeTest import SmokeTest, ButtonFinder, TdLabelFinder, DivTextFinder, SpanTextFinder
from smoketest.SmokeTest import TableColumnHeaderFinder
from smoketest.SmokeTest import TableRowHeaderFinder
from optparse import OptionParser
from enum import Enum


def main():
    parser = OptionParser(usage="usage: %prog ipAddress browser")
    # parser.add_option("-c", "--chelp", help="Add arguments for IP Address for radio and target browser")
    (options, args) = parser.parse_args()
    print('args', args)
    if len(args) != 3:
        parser.error("wrong number of arguments")

    GlobalFuncs.set_path(args[2])
    TEST_TYPE = 'smoketest'

    run_all = RunAll(TEST_TYPE)
    run_all.run_all()

    # try:
    #     run_all.run_all()
    # finally:
    #     Utils.print_tree(Utils.log_dir())

    # Utils.generate_overall_result(Utils.log_dir(), TEST_TYPE)


class ComparisonResult(Enum):
    LATEST = 1
    ACTIVE = 2
    SAME = 3


def reformat_for_compare(swpack):
    # if build is master substitute master for 99.99.99 for easier comparison
    if swpack.find('master') != -1:
        return swpack.replace('master', '99.99.99')
    else:
        return swpack


def must_download_latest(active_swpack, latest_swpack):
    active = active_swpack.split('.')
    decoded_latest = latest_swpack.encode('ascii', 'ignore')
    latest = decoded_latest.split('.')
    res = None

    for i in range(0, min(len(active), len(latest))):
        if compare(int(active[i]), int(latest[i])) == ComparisonResult.SAME or compare(int(active[i]), int(
                latest[i])) == ComparisonResult.ACTIVE:
            res = False
        else:
            res = True
    return res


def compare(active, latest):
    if active < latest:
        return ComparisonResult.LATEST
    elif active > latest:
        return ComparisonResult.ACTIVE
    else:
        return ComparisonResult.SAME


def determine_latest_swpack(active_swpack, latest_swpack):
    active = active_swpack.split('.')
    decoded_latest = latest_swpack.encode('ascii', 'ignore')
    latest = decoded_latest.split('.')

    for i in range(0, min(len(active), len(latest))):
        if compare(int(active[i]), int(latest[i])) == 'same':
            continue
        elif compare(int(active[i]), int(latest[i])) == 'active':
            return 'active'
        else:
            return 'latest'
    return len(active) > len(latest)


class RunAll:
    def __init__(self, test_type):
        self.test_type = test_type
        self.dir = Utils.log_dir()
        self.test_log = TestLog(self.dir)
        self.driver = Utils.create_driver(sys.argv[2])
        self.utils = Utils(self.driver, self.test_log)
        print('init')

    def run_all(self):

        self.run_smoke_test()
        # active_sw_version = Utils.get_active_sw_version()
        # latest_swpack = Utils.get_latest_sw_pack_version()
        #
        # # dummies for tests
        # active_sw_version = '3.6.1(41.5629)' #'master.12.1919'
        # latest_swpack = active_sw_version  # 'master.12.1919'
        #
        # swpack = determine_latest_swpack(reformat_for_compare(active_sw_version), reformat_for_compare(latest_swpack))
        # get_latest = must_download_latest(reformat_for_compare(active_sw_version), reformat_for_compare(latest_swpack))
        #
        # if get_latest:
        #     print ('Get latest sw pack...')
        #     Utils.upload_latest(self.run_smoke_test)
        # else:
        #     print ('Using latest, don\'t need to upload latest... ')
        #     self.run_smoke_test()
        #     # self.write_config_test(self.driver)

    @staticmethod
    def expand_folders(driver):
        hasUnopened = True

        while hasUnopened:
            folders = driver.find_elements_by_xpath("//div[@class='side_menu_folder']")
            hasUnopened = False
            for folder in folders:

                collapsed = len(folder.find_elements_by_xpath("div[@class='side_menu_toggle collapsed']")) > 0
                if folder.is_displayed() and collapsed:
                    name = folder.text
                    driver.execute_script("arguments[0].scrollIntoView(true);", folder)
                    time.sleep(2)
                    search = "//div[normalize-space(.)='" + name + "']/div[@class='side_menu_toggle collapsed']"
                    folder = folder.find_elements_by_xpath(search)[0]
                    folder.click()
                    search = "//div[normalize-space(.)='" + name + "']/div[@class='side_menu_toggle expanded']"
                    WebDriverWait(driver, 35).until(EC.presence_of_element_located((By.XPATH, search)))

                    hasUnopened = True
                    break

    @staticmethod
    def get_screens(driver):
        RunAll.expand_folders(driver)
        items = driver.find_elements_by_xpath("//a[@class='side_menu_entry']")

        result = []
        for item in items:
            path = [item.text]
            container = item.find_element(By.XPATH, "..")
            folders = container.find_elements_by_xpath("preceding-sibling::div[1]")

            while len(folders) > 0:
                path.insert(0, folders[0].text)
                container = container.find_element(By.XPATH, "..")
                folders = container.find_elements_by_xpath("preceding-sibling::div[@class='side_menu_folder'][1]")
            result.append("/".join(path))

        return result

    def run_smoke_test(self):
        # print('Gonna run the smoketests...')
        # driver = Utils.create_driver(sys.argv[2])
        # utils = Utils(driver, self.test_log)
        self.utils.delete_existing_dir()

        self.test_log.start('login')
        test_helper = TestHelper(self.test_log, self.driver, self.test_type, self.utils)
        login_handler = LoginHandler(self.driver, test_helper, self.test_log)
        login_handler.start()

        print('log', self.test_log, self.utils.log_dir())
        # test_log = TestLog(self.dir)

        # Uncomment this to get coverage graph
        # test_log.add_num_screens(RunAll.get_num_screens(self.driver))
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'menu_node_equipment')))
        # self.driver.find_element_by_id('menu_node_equipment').click()

        smoke_test = SmokeTest(self.driver, self.test_log, test_helper)
        try:
            side_menu = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located((By.CLASS_NAME, "side_menu_folder")))
        except e:
            test_helper.assert_false(True, "unable to find side menu", "side_menu")
            login_handler.end()
            self.test_log.close()
            raise e


        tests = RunAll.get_screens(self.driver)

        smoke_test.create("Status/Alarms")
        smoke_test.create("System Configuration/Admin/Users")
        smoke_test.create("Status/Manufacture Details")
        # smoke_test.create("Status/Event Log")
        # smoke_test.create("Switching & Routing Configuration/Port Manager")
        # smoke_test.create("Switching & Routing Configuration/Interfaces")

        # for test in tests:
        #     try:
        #         if not smoke_test.create(test):
        #             return False
        #     except Exception as ex:
        #         # error_file.write("Failed running: " + test + ex + '\r\n')
        #         print("Failed running ", test, ex)

        # return True

        login_handler.end()
        self.test_log.close()


if __name__ == "__main__":

    count = 0
    # while 1:
    for x in xrange(1):
        # time.sleep(5)
        # main()
        try:
            time.sleep(5)
            main()
            count += 1
            print("Run " + str(count) + " times.")
        except Exception as e:
            import signal

            print("Main loop exception")

            traceback.print_exc()
            print("About to kill process: ", os.getpid())
            # os.kill(os.getpid(), signal.SIGBREAK)

    # main()
