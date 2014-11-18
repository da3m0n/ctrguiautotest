from selenium.webdriver.common.by import By
from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils
import sys


def main():
    driver = Utils.create_driver(sys.argv[2])
    log_dir = Utils.log_dir()
    Utils.delete_existing_logfile(log_dir)
    test_log = TestLog(SoftwareManagement, log_dir)
    # create instance of class here and then  run method of class 
    sw_management = SoftwareManagement(IsolatedLoginHandler())
    sw_management.run_software_management(driver, test_log)
    test_log.close()


class SoftwareManagement():
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def run_software_management(self, driver, test_log):
        gui_lib = Utils(driver)
        self.login_manager.login()

        test_log.start('SoftwareManagement')
        test_helper = TestHelper(test_log, driver)

        driver.switch_to_default_content()
        gui_lib.click_element('menu_node_system_tree')
        gui_lib.click_element('menu_node_admin_tree')
        gui_lib.click_element('menu_node_swload')

        driver.switch_to_frame('frame_content')

        sw_status_label = driver.find_element(By.XPATH, "//body/fieldset[1]/legend").text
        test_helper.assert_true(len(sw_status_label) <= 0,
                                'Expected ' + sw_status_label + ' to be > 0, but was ' + str(len(sw_status_label)),
                                'Check ' + sw_status_label + ' visible')

        sw_upgrade_label = driver.find_element(By.XPATH, "//body/fieldset[2]/legend").text
        test_helper.assert_true(len(sw_upgrade_label) <= 0,
                                'Expected ' + sw_upgrade_label + ' to be > 0, but was ' + str(len(sw_upgrade_label)),
                                'Check ' + sw_upgrade_label + ' visible')

        active_version = gui_lib.find_element_by_id('SoftwareLoadingStatusWidget1_version').text
        test_helper.assert_true(len(active_version) <= 0,
                                'Expected ' + active_version + ' to be > 0, but was ' + str(len(active_version)),
                                'Check Active version visible')

        inactive_version = gui_lib.find_element_by_id('SoftwareLoadingStatusWidget1_inactiveversion').text
        test_helper.assert_true(len(inactive_version) <= 0,
                                'Expected ' + inactive_version + ' to be > 0, but was ' + str(len(inactive_version)),
                                'Check Inactive version visible')

        rollback_btn = gui_lib.find_element_by_id('SoftwareLoadingStatusWidget1_rollback').text
        test_helper.assert_true(len(rollback_btn) <= 0, 'Expected Rollback button to be displayed, was not',
                                'Check Rollback button displayed')

        status = gui_lib.find_element_by_id('SoftwareUpgradeWidget1_status').text
        test_helper.assert_true(len(status) <= 0, 'Expected Status to be displayed, was not',
                                'Check Status displayed')

        start_btn = gui_lib.find_element_by_id('SoftwareUpgradeWidget1_start').text
        test_helper.assert_true(len(start_btn) <= 0, 'Expected Start button to be displayed, was not',
                                'Check Start button displayed')

        self.login_manager.logout()


if __name__ == '__main__':
    main()
