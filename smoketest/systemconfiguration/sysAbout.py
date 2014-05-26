import sys
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils


def main():
    Utils.delete_existing_logfile()
    about = SystemAbout(IsolatedLoginHandler())
    test_log = TestLog('System About')
    about.run_system_about(Utils.create_driver(sys.argv[2]), test_log)
    print('Inside system about')


class SystemAbout(object):
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def run_system_about(self, driver, test_log):
        gui_lib = Utils()

        self.login_manager.login(driver)
        test_log.start('System About')

        test_helper = TestHelper(test_log)

        usr = "root"
        pw = "admin123"
        timetup = time.localtime()
        iso = time.strftime('%Y-%m-%d %H:%M:%S ', timetup)
        print "=====", iso, "====="

        driver.switch_to_default_content()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "menu_node_7_tree")))

        driver.find_element_by_id("menu_node_7_tree").click()
        time.sleep(2)
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "menu_node_10")))
        driver.find_element_by_id("menu_node_10").click()
        driver.switch_to_frame("frame_content")

        # about = driver.find_element(By.XPATH, "//body/fieldset/legend").text
        # assert about == "About", ("Expected About but got ", about)

        # title = 'Aviat Networks Converged Transport Router'
        # webTitle = driver.find_element_by_xpath('//body/fieldset/div/div/h3').text
        # assert title == webTitle, ('Expected ', title, ' but got ', webTitle)
        #
        # # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'licenses')))
        # time.sleep(2)

        licenses = gui_lib.find_element(driver, 'licenses')  #driver.find_element_by_id('licenses')
        # driver.execute_script("document.getElementById('licenses').innerHTML=\"\";")
        test_helper.assert_true(len(licenses.text) == 0, 'Expected SW Version to be > 0',
                               'Checking Licenses text not empty')

        time.sleep(2)
        self.login_manager.logout(driver)
        test_log.close()


if __name__ == "__main__":
    main()