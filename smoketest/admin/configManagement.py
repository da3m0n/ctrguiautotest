import sys
from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils


def main():
    log_dir = Utils.log_dir()
    config_management = ConfigManagement(IsolatedLoginHandler())
    test_log = TestLog('Config Management', log_dir)
    config_management.run_config_management(Utils.create_driver(sys.argv[2]), test_log)
    test_log.close()

class ConfigManagement():
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def run_config_management(self, driver, test_log):
        gui_lib = Utils(driver)

        self.login_manager.login()

        test_log.start('Config Management')
        test_helper = TestHelper(test_log, driver)

        driver.switch_to_default_content()
        gui_lib.click_element('menu_node_system_tree')
        gui_lib.click_element('menu_node_admin_tree')
        gui_lib.click_element('menu_node_config_management')

        driver.switch_to_frame('frame_content')

        download_btn = gui_lib.find_element_by_id('download')
        # driver.execute_script("document.getElementById('download').style.visibility='hidden'")
        test_helper.assert_true(len(download_btn.text) <= 0, 'Button has no text', 'Button text visible')
        test_helper.assert_true(download_btn.is_displayed() == False, 'Download button not displayed', 'Download button visible onscreen')
        self.login_manager.logout()

if __name__ == '__main__':
    main()
