from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
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
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, 'PseudowireSettingsWidget1_TW_0_1_renderer')))

        switch_mac = driver.find_element_by_id('PseudowireSettingsWidget1_TW_0_1_renderer').text
        # driver.execute_script("document.getElementById('PseudowireSettingsWidget1_TW_0_1_renderer').innerHTML=\"\";")
        test_helper.assert_true(len(switch_mac) == 0, 'Expected Switch MAC to be > 0 but was ' + str(len(switch_mac)),
                                'Check Switch MAC visible')

        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'PseudowireWidget1_TW_table')))
        table = driver.find_element_by_id('PseudowireWidget1_TW_table')
        header_ids = table.find_elements_by_tag_name('th')
        header_inner_html = Utils.build_inner_html_array(Utils.build_id_array(table))

        # store these names before they potentially get removed
        header_names = []
        for header in header_ids:
            header_names.append(header.text)

        # # these tests only check that headers are displayed. Wont flag if there are any missing, it's all or none
        # uncomment to remove headers for testing
        headers_removed = False
        # for inner_html in header_inner_html:
        #     driver.execute_script(inner_html)
        #     headers_removed = True

        #  if necessary get the headers again
        if headers_removed:
            header_ids = table.find_elements_by_tag_name('th')

        missing_headers = []
        iter_headers = iter(header_ids)
        next(iter_headers)  # to skip first element as it's always blank
        for header in iter_headers:
            if header.text == '':
                missing_headers.append(header)

        test_helper.assert_true(len(missing_headers) > 0, 'Expected Headers, got None', 'Testing Headers')

        self.login_manager.logout()


if __name__ == '__main__':
    main()
