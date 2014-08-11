import selenium
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, InvalidSelectorException
from selenium.webdriver.support.expected_conditions import _element_if_visible, _find_element, _find_elements
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from smoketest.TestHelper import TestHelper
from smoketest.mylib.utils import Utils


class SmokeTest():
    def __init__(self, driver, test_log):
        self.test_log = test_log
        self.driver = driver
        self.gui_lib = Utils(driver)
        self.test_helper = TestHelper(self.test_log, self.driver)

    def create(self, screen_name, items_to_test):
        breadcrumbs = screen_name.split('/')
        self.__navigate_to_location(breadcrumbs)
        self.driver.switch_to_frame('frame_content')

        self.test_log.start(breadcrumbs[-1])
        # time.sleep(4)
        # self.driver.execute_script("document.getElementById('DateTimeWidget1_TW_3_1').innerHTML=\"\";")

        vals_combined = dict()
        for item in items_to_test:
            try:
                # time.sleep(5)
                # test = self.driver.find_element_by_id('DateTimeWidget1_TW_0')
                # print('test', test)
                label_name = WebDriverWait(self.driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, "//th[contains(text(),'" + item + "')]")))

                self.__does_match(item, label_name.text)

                # self.driver.execute_script("document.getElementById('DateTimeWidget1_TW_0').innerHTML=\"\";")
                label_value = label_name.find_element_by_xpath("following-sibling::td").text
                vals_combined.update({label_name.text: label_value})
                # res = self.__testItems(item, label_name, label_value)
            except TimeoutException:
                self.test_helper.assert_true(True,
                                             'Expected ' + item + ' but TimeoutException occurred.',
                                             'Ensure ' + item + ' to be visible')
                break
            except MisMatchException as e:
                self.test_helper.assert_true(True,
                                             'Expected ' + e.errors[0] + ' but was ' + e.errors[1],
                                             'Ensure ' + e.errors[0] + ' to be visible')
                break

        for key, val in vals_combined.iteritems():
            self.test_helper.assert_true(len(key) == 0,
                                         'Expected ' + key + ' to be > 0 but was ' + str(len(key)),
                                         'Ensure ' + key + ' label visible')
            self.test_helper.assert_true(len(val) == 0,
                                         'Expected ' + val + ' to be > 0 but was ' + str(len(val)),
                                         'Ensure ' + key + ' value visible')

    @staticmethod
    def __does_match(item, text):
        if item != text:
            raise MisMatchException("Expected " + item + " but got " + text, (item, text))

    def __navigate_to_location(self, breadcrumbs):
        self.driver.switch_to_default_content()
        self.__navigate_to_location_rec(self.driver, breadcrumbs)

    def __navigate_to_location_rec(self, root, breadcrumbs):
        breadcrumb = breadcrumbs[0]
        if len(breadcrumbs) == 1:
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.LINK_TEXT, breadcrumbs[0])))
            last_el = self.driver.find_element_by_link_text(breadcrumbs[0])
            last_el.click()
        else:
            folder = WebDriverWait(root, 20).until(
                my_visibility_of_elements((By.XPATH, "//div[@class='side_menu_folder']"), breadcrumb))
            expanded = len(folder.find_elements_by_class_name('expanded')) > 0
            if not expanded:
                folder.click()
            self.__navigate_to_location_rec(folder, breadcrumbs[1:])


class MisMatchException(Exception):
    def __init__(self, message, errors):

        Exception.__init__(self, message)
        self.errors = errors

class my_visibility_of_elements(object):
    def __init__(self, locator, name):
        self.locator = locator
        self.name = name

    def __call__(self, driver):
        try:
            folders = _find_elements(driver, self.locator)
            for folder in folders:
                # time.sleep(0.25)
                if folder.is_displayed():
                    if folder.text == self.name:
                        return folder

            return False
        except StaleElementReferenceException:
            return False


