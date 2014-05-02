import sys
import time
from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils


def main():
    Utils.delete_existing_logfile()
    manu_details = ManufactureDetails(IsolatedLoginHandler())
    test_log = TestLog('Manufacture Details')
    manu_details.run_manufacture_details(Utils.create_driver(sys.argv[2]), test_log)


class ManufactureDetails(object):
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def run_manufacture_details(self, driver, test_log):
        self.login_manager.login(driver)
        gui_lib = Utils()
        test_helper = TestHelper(test_log)

        test_log.start('Manufacture Details')

        driver.switch_to_default_content()
        gui_lib.click_element(driver, 'menu_node_7_tree')
        gui_lib.click_element(driver, 'menu_node_11')

        driver.switch_to_frame('frame_content')
        manu_details = driver.find_element_by_id('ManufactureDetailsWidget1_content').text
        test_helper.assert_true(len(manu_details) == 0, 'Manufacture Details not visible',
                                'Test Manufacture Details')

        # TestHelper.tear_down(driver)

        self.login_manager.logout(driver)
        test_log.close()


if __name__ == '__main__':
    main()
