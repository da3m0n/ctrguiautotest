from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sys
from selenium.webdriver.support.wait import WebDriverWait
from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils


def main():
    print('main')
    driver = Utils.create_driver(sys.argv[2])
    log_dir = Utils.log_dir()
    alarms = Alarms(IsolatedLoginHandler(driver))
    test_log = TestLog('Alarms', log_dir)
    alarms.run_alarms(driver, test_log)
    test_log.close()


class Alarms():
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def run_alarms(self, driver, test_log):
        gui_lib = Utils(driver)

        self.login_manager.login()

        test_log.start('Alarms')
        test_helper = TestHelper(test_log, driver)

        driver.switch_to_default_content()
        gui_lib.click_element('menu_node_status')
        gui_lib.click_element('menu_node_alarms')

        driver.switch_to_frame('frame_content')
        # t = driver.find_element(By.XPATH, "//body/fieldset/legend").text
        # print('test', t)
        buttons = driver.find_elements_by_tag_name('button')
        # try test for visibility on the function below as it finds the buttons
        # before they are onscreen
        # (EC.visibility_of_element_located(
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button')))


        # check that there are 3 buttons
        test_helper.assert_true(len(buttons) != 3, 'Not all buttons displayed', 'Check that all buttons displayed')

        # test that the buttons have text on them
        for btn in buttons:
            test_helper.assert_true(len(btn.text.strip()) == 0, 'No text on button', 'Check buttons have text')
            print(len(btn.text.strip()))

        test_log.close()
        self.login_manager.logout()


if __name__ == '__main__':
    main()
