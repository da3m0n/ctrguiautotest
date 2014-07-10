from selenium.webdriver.common.by import By
import sys
from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils


def main():
    print('main')
    log_dir = Utils.log_dir()
    alarms = Alarms(IsolatedLoginHandler())
    test_log = TestLog('Alarms', log_dir)
    alarms.run_alarms(Utils.create_driver(sys.argv[2]), test_log)
    test_log.close()


class Alarms():
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def run_alarms(self, driver, test_log):
        gui_lib = Utils()

        self.login_manager.login(driver)

        test_log.start('Alarms')
        test_helper = TestHelper(test_log, driver)

        driver.switch_to_default_content()
        t = driver.find_element(By.XPATH, "//body/fieldset/legend/div/div/")
        print('test', t)




if __name__ == '__main__':
    main()
