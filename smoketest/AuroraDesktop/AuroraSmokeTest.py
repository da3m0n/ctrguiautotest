from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.expected_conditions import _find_elements
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from aurorasmoketest.utils import Utils

import sys
class AuroraSmokeTest():
    def __init__(self, driver):
        self.driver = driver
        self.gui_lib = Utils(driver)

    def navigate_to_screen(self, screen_name):
        self.__navigate_to_location(screen_name)

    def __navigate_to_location(self, screen_name):
		self.driver.switch_to_default_content()
		print("http://"+sys.argv[1]+":"+sys.argv[2]+"/"+screen_name)
		self.driver.get("http://"+sys.argv[1]+":"+sys.argv[2]+"/"+screen_name)
		WebDriverWait(screen_name, 20).until(my_visibility_of_elements((By.ID, screen_name
		), self.driver, screen_name))
		#WebDriverWait(screen_name, 20)		
class my_visibility_of_elements(object):
    def __init__(self, locator, driver, name):
        self.locator = locator
        self.driver = driver
        self.name = name

    def __call__(self, page):
        try:
            _find_elements(self.driver, self.locator)
            #WebDriverWait(self.name, 20).until(self.driver.find_element_by_id("content"))
            return False
        except StaleElementReferenceException:
            return False
