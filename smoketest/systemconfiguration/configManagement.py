from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils
import sys


def main():
    driver = Utils.create_driver(sys.argv[2])
    log_dir = Utils.log_dir()
    Utils.delete_existing_logfile(log_dir)
    test_log = TestLog(ConfigManagement, log_dir)
    # create instance of class here and then  run method of class 
    config = ConfigManagement(IsolatedLoginHandler(driver))
    config.run_config_management(driver, test_log)
    test_log.close()


class ConfigManagement():
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def run_config_management(self, driver, test_log):
        gui_lib = Utils(driver)
        self.login_manager.login()

        test_log.start(ConfigManagement)
        test_helper = TestHelper(test_log, driver)

        driver.switch_to_frame('frame_content')

        download_btn = gui_lib.find_element_by_id('download').text
        download_btn_len = len(download_btn)
        test_helper.assert_true(download_btn_len > 0, 'Expected Download button text > 0 but was ' + download_btn_len,
                                'Ensure button has text')

        test = 'sends'
        restore_btn = driver.find_element_by_class_name(test).text
        restore_btn_len = len(restore_btn)
        test_helper.assert_true(restore_btn_len > 0, 'Expected Restore button text > 0 but was ' + restore_btn_len,
                                'Ensure button has text')

        test_log.close()
        self.login_manager.logout()


if __name__ == '__main__':
    main()
