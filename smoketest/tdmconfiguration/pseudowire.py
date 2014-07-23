from selenium.webdriver.common.by import By
from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils
import sys


def main():
    driver = Utils.create_driver(sys.argv[2])
    log_dir = Utils.log_dir()
    # Utils.delete_existing_logfile(log_dir)
    test_log = TestLog(PseudoWire, log_dir)
    # create instance of class here and then  run method of class 
    pseudo_wire = PseudoWire(IsolatedLoginHandler(driver))
    pseudo_wire.run_pseudo_wire(driver, test_log)
    test_log.close()


class PseudoWire():
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def run_pseudo_wire(self, driver, test_log):
        gui_lib = Utils(driver)
        self.login_manager.login()

        test_log.start('PseudoWire')
        test_helper = TestHelper(test_log, driver)

        driver.switch_to_default_content()
        gui_lib.click_element('menu_node_tdm_tree')
        gui_lib.click_element('menu_node_pseudowire')

        driver.switch_to_frame('frame_content')
        pseudowire_global_label = driver.find_element(By.XPATH, "//body/fieldset[1]/legend").text
        test_helper.assert_true(len(pseudowire_global_label) == 0,
                                'Expected ' + pseudowire_global_label + ' to be > 0, but was ' + str(
                                    len(pseudowire_global_label)),
                                'Check ' + pseudowire_global_label + ' visible')

        pseudowire_config_label = driver.find_element(By.XPATH, "//body/fieldset[2]/legend").text
        test_helper.assert_true(len(pseudowire_config_label) == 0,
                                'Expected ' + pseudowire_config_label + ' to be > 0, but was ' + str(
                                    len(pseudowire_config_label)),
                                'Check ' + pseudowire_config_label + ' visible')

        self.login_manager.logout()


if __name__ == '__main__':
    main()
