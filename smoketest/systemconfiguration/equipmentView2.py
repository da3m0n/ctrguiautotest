import sys

from selenium.webdriver.common.by import By

from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils


def main():
    Utils.delete_existing_logfile()
    test_log = TestLog('Equipment View')
    equip_view = EquipmentView(IsolatedLoginHandler())
    equip_view.run_equipment_view(Utils.create_driver(sys.argv[2]), test_log)


class EquipmentView(object):
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def run_equipment_view(self, driver, test_log):
        self.login_manager.login(driver)
        gui_lib = Utils()
        test_helper = TestHelper(test_log)

        test_log.start('Equipment View')

        prodDescription = driver.find_element(By.ID, "top_menu_product_description").text

        driver.switch_to_frame("frame_content")

        # driver.execute_script("document.getElementById('ChassisViewWidget1_container').innerHTML=\"\";")
        chassis = driver.find_element_by_id('ChassisViewWidget1_container')
        test_helper.assert_true(len(chassis.text) == 0, 'Expected chassis to be displayed but was not',
                               'Ensure Chassis displayed')

        # # click on Sensors
        # driver.find_element_by_id("menu_node_4").click()
        # time.sleep(4)
        # driver.switch_to_frame("frame_content")
        #
        # table = driver.find_element(By.ID, "tableWidget1_table")
        # titles = driver.find_elements_by_class_name("RenderersGroupingCellContainer")

        # perhaps refactor the asserts below this block using this object??
        # sensors = {
        #     "chassis": prodDescription + " chassis",
        # "fan": "FAN Tray (Slot 6)", "pwr": "PWR plugin in module (Slot 1)",
        #     "rac_x2": "RACx2 plug in module (Slot 2)", "interface1": "Radio Interface 1/2/1",
        #     "interface2": "Radio Interface 1/2/2"
        # }
        #
        # for title in titles:
        #     print(title.text, sensors)
        #         # assert title.text == val, ("Expected ", titles[0].text, " but got ", val)

        # chassis = prodDescription + " chassis"
        # fan = "FAN Tray (Slot 6)"
        # pwr = "PWR plugin in module (Slot 1)"
        # rac_x2 = "RACx2 plug in module (Slot 2)"
        # interface1 = "Radio Interface 1/2/1"
        # interface2 = "Radio Interface 1/2/2"
        #
        # assert titles[0].text == chassis, ("Expected ", titles[0].text, " but got ", chassis)
        # assert titles[1].text == fan, ("Expected ", titles[1].text, " but got ", fan)
        # assert titles[2].text == pwr, ("Expected ", titles[2].text, " but got ", pwr)
        # assert titles[3].text == rac_x2, ("Expected ", titles[3].text, " but got ", rac_x2)
        # assert titles[4].text == interface1, ("Expected ", titles[4].text, " but got ", interface1)
        # assert titles[5].text == interface2, ("Expected ", titles[5].text, " but got ", interface2)

        # Event Log
        # driver.switch_to_default_content()
        # driver.find_element_by_id("menu_node_5").click()
        # time.sleep(2)

        # Reports
        # driver.switch_to_default_content()
        # driver.find_element_by_id("menu_node_6").click()
        # driver.switch_to_frame("frame_content")
        #
        # try:
        #     reports = driver.find_element(By.XPATH, "//body/fieldset/legend").text
        #     assert reports == "Reports", ("Expected Reports but got ", reports)
        #     generate = driver.find_element(By.ID, "helpdesk_create").text
        #     assert generate == "Generate", ("Expected Generate but got ", generate)
        # except "Element Not Found Exception":
        #     print "Element Not Found Exception"
        # time.sleep(2)

        # Manufacture Details
        # driver.switch_to_default_content()
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "menu_node_7_tree")))
        # time.sleep(2)
        # driver.find_element_by_id("menu_node_7_tree").click()
        # driver.find_element_by_id("menu_node_11").click()
        # time.sleep(2)

        # Software Management
        # guiLib.find_element(driver, 'menu_node_7_tree')
        # guiLib.find_element(driver, 'menu_node_14_tree')
        # guiLib.find_element(driver, 'menu_node_14')
        # guiLib.find_element(driver, 'menu_node_16')
        # driver.switch_to_frame('frame_content')
        #
        # downloadBtn = driver.find_element_by_id('SoftwareLoadingStatusWidget1_version').size > 0
        # assert downloadBtn, ('Expected to find a Download but found none', downloadBtn)
        # WebDriverWait(driver, 20).until(
        #     EC.visibility_of_element_located((By.ID, 'SoftwareLoadingStatusWidget1_version')))
        # activeVersion = driver.find_element_by_id('SoftwareLoadingStatusWidget1_version').text
        # activeVersionLen = len(activeVersion)
        # assert activeVersionLen > 0, ('The Active version was expected to be > 0 but was', activeVersionLen)
        #
        # print('active', activeVersion)
        # time.sleep(2)

        # # License Management
        # driver.find_element_by_id("menu_node_17").click()
        # time.sleep(2)
        #
        # # Ethernet Configuration
        # driver.find_element(By.ID, "menu_node_18_tree").click()
        # # Port Manager
        # driver.find_element_by_id("menu_node_19").click()
        # time.sleep(2)
        #
        # # Radio Configuration
        # driver.find_element(By.ID, "menu_node_20_tree").click()
        # # Radio Link Configuration
        # driver.find_element_by_id("menu_node_21").click()
        # time.sleep(2)
        #
        # # Radio Link Diagnostics
        # driver.find_element_by_id("menu_node_22").click()
        # time.sleep(2)
        #
        # # Radio Link Protection
        # driver.find_element_by_id("menu_node_23").click()
        # time.sleep(2)
        #
        # # Radio Protection Diagnostics
        # driver.find_element_by_id("menu_node_24").click()
        # time.sleep(2)
        #
        #
        # # TDM Configuration
        # driver.find_element(By.ID, "menu_node_25_tree").click()
        # # Tributary Diagnostics
        # driver.find_element_by_id("menu_node_26").click()
        # time.sleep(2)
        #
        # # Statistics
        # driver.find_element(By.ID, "menu_node_27_tree").click()
        # # Interface
        # driver.find_element_by_id("menu_node_28").click()
        # time.sleep(2)
        #
        # # Ethernet
        # driver.find_element_by_id("menu_node_29").click()
        # time.sleep(2)
        #
        # # Radio Link Performance
        # driver.find_element_by_id("menu_node_30").click()
        # time.sleep(2)
        #
        # # Radio Link History
        # driver.find_element_by_id("menu_node_31").click()
        # time.sleep(2)
        #
        # # ARP Cache
        # driver.find_element_by_id("menu_node_32").click()
        # time.sleep(2)
        #
        # # MAC Address Table
        # driver.find_element_by_id("menu_node_33").click()
        # time.sleep(2)

        # driver.switch_to_default_content()
        # guiLib.logout(driver)

        self.login_manager.logout(driver)
        test_log.close()


if __name__ == "__main__":
    main()



