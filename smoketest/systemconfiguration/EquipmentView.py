import sys
from selenium.webdriver.common.by import By
from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils


def main():
    print 'in main'
    log_dir = Utils.log_dir()
    equip_view = EquipmentView(IsolatedLoginHandler())
    test_log = TestLog('Equipment View', log_dir)
    equip_view.run_equipment_view(Utils.create_driver(sys.argv[2]), test_log)
    test_log.close()


class EquipmentView():
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def run_equipment_view(self, driver, test_log):
        gui_lib = Utils()

        self.login_manager.login(driver)
        test_helper = TestHelper(test_log, driver)
        test_log.start('Equipment View')

        driver.switch_to_default_content()
        prodDescription = driver.find_element(By.ID, "top_menu_product_description").text

        driver.switch_to_frame("frame_content")

        chassis = gui_lib.find_element_by_id(driver, 'ChassisViewWidget1_container')
        # driver.execute_script("document.getElementById('ChassisViewWidget1_container').innerHTML=\"\";")
        # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, chassis)))

        test_helper.assert_true(len(chassis.text) == 0, 'Expected chassis to be displayed but was not',
                                'Ensure Chassis displayed')

        self.login_manager.logout(driver)


if __name__ == '__main__':
    main()