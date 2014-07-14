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
        download_btn_len = len(download_btn.text)
        test_helper.assert_true(download_btn_len <= 0,
                                'Expected Download button text > 0 but was ' + str(download_btn_len),
                                'Ensure button has text')

        # driver.execute_script("document.getElementById('download').style.visibility='hidden'")
        test_helper.assert_true(download_btn.is_displayed() == False, 'Download button not displayed',
                                'Download button visible onscreen')

        restore_btn = driver.find_element_by_class_name('sends').text
        restore_btn_len = len(restore_btn)
        test_helper.assert_true(restore_btn_len <= 0,
                                'Expected Restore button text > 0 but was ' + str(restore_btn_len),
                                'Ensure button has text')

        table = driver.find_element_by_class_name('config_inner')
        radio_btns = table.find_elements_by_tag_name('label')
        restore_options_list = []
        for btn in radio_btns:
            restore_options_list.append(btn.text)

        for i in range(len(restore_options_list)):
            restore_label = restore_options_list[i]
            restore_labels_len = len(restore_label)
            test_helper.assert_true(restore_labels_len <= 0,
                                    'Expected ' + restore_label + ' to be > 0 but was ' + str(restore_labels_len),
                                    'Ensure ' + restore_label + ' visible')

        test_log.close()
        self.login_manager.logout()


if __name__ == '__main__':
    main()
