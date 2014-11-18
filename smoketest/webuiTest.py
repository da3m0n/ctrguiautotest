#!/usr/bin/env python
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import _find_elements
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
import time, re
import mylib
# import MyConfig
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, InvalidSelectorException
# from selenium.webdriver.support.expected_conditions import _element_if_visible, _find_element, _find_elements

# mycfg = MyConfig(cfgfile="config.cfg")

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

def wait(driver, selector):
    print "Waiting"
    #WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
    #WebDriverWait(driver, 30).until(EC.presence_of_element_located(By.ID, selector))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, selector)))
    #abel_name = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(By.ID, "layout_device_name"))
    #EC.presence_of_element_located((By.ID, "layout_device_name"))

    print "Done Waiting"


#time.sleep(5)
def logout(ip, gambit, drivers):
    for driver in drivers:
        driver.get("http://" + ip + "/logout")


def quit(drivers):
    for driver in drivers:
        driver.quit()

def loadPage(menuTarget, waitSelector, drivers):
    driver = drivers[0]
    driver.switch_to_default_content()
    driver.find_element_by_id(menuTarget).click()

        # wait(driver, waitSelector)
    # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, waitSelector)))

    # for driver in drivers:
    #     # driver.switch_to_default_content()
    #     # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, waitSelector)))
    #     driver.find_element_by_id(menuTarget).click()
        # wait(driver, waitSelector)
        # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, waitSelector)))
    # time.sleep(10)


def menuSectionClick(node, drivers):
    for driver in drivers:
        driver.find_element_by_id(node).click()
        time.sleep(2)


def setSize(drivers):
    for arg in drivers:
        arg.set_window_size(1024, 768)

def login(url, drivers):
    for driver in drivers:
        driver.get(url)
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("root")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("admin123")
        driver.find_element_by_name("submit").click()


def loadURL(url, drivers):
    for driver in drivers:
        driver.get(url)

def test():
    # configs = [mycfg.dev1]
    # for config in configs:
    # driver1 = webdriver.Chrome("C:\ChromeDriver\chromedriver.exe") #webdriver.Firefox()
    driver1 = webdriver.Firefox()
    #driver2 = webdriver.Firefox()
    #driver3 = webdriver.Firefox()
    #driver4 = webdriver.Firefox()
    #drivers = [driver1, driver2, driver3, driver4];
    drivers = [driver1]

    try:
        setSize([driver1])
        # base_url = "http://" + config.ipaddress + "/"
        login("http://10.16.13.50/", [driver1])
        time.sleep(5)
        #switchToDefaultContent(drivers)
        WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.ID, "layout_device_name")))
        gambit = ""
        allCookies = driver1.get_cookies()

        for cookie in allCookies:
            if (cookie['name'] == "gambit"):
                gambit = cookie["value"]

        WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.ID, "menu_node_status")))

        menuSectionClick("menu_node_status_tree", drivers)
        loadPage("menu_node_alarms", "content", drivers)  #menu_node_alarms
        loadPage("menu_node_sensors", "content", drivers)  #menu_node_sensors
        # loadPage("menu_node_event_log", "content", drivers)  #menu_node_event_log
        # loadPage("menu_node_reports", "fieldset", drivers)  #menu_node_reports
        # loadPage("menu_node_manufacture", "fieldset", drivers)  #menu_node_reports
        menuSectionClick("menu_node_system_tree", drivers)
        # menuSectionClick("menu_node_network_synchronization_tree", drivers)

        # loadPage("menu_node_system_info", "fieldset", drivers)
        # loadPage("menu_node_date_time", "fieldset", drivers)
        # loadPage("menu_node_poe_config", "fieldset", drivers)
        # loadPage("menu_node_backup_power", "fieldset", drivers)
        # menuSectionClick("menu_node_admin", drivers)
        # loadPage("menu_node_config_management", "fieldset", drivers)
        # loadPage("menu_node_swload", "fieldset", drivers)
        # loadPage("menu_node_licensing", "fieldset", drivers)
        menuSectionClick("menu_node_ethernet_tree", drivers)
        # loadPage("menu_node_port_management", "fieldset", drivers)
        menuSectionClick("menu_node_radio_tree", drivers)
        # loadPage("menu_node_radio_config", "fieldset", drivers)
        # loadPage("menu_node_radio_diag", "fieldset", drivers)
        # loadPage("menu_node_radio_prot_config", "fieldset", drivers)
        # loadPage("menu_node_radio_prot_diag", "fieldset", drivers)
        menuSectionClick("menu_node_tdm_tree", drivers)
        # loadPage("menu_node_trib_diag", "fieldset", drivers)
        menuSectionClick("menu_node_statistics_tree", drivers)
        # loadPage("menu_node_stats_interface", "fieldset", drivers)
        # loadPage("menu_node_stats_ethernet", "fieldset", drivers)
        # loadPage("menu_node_stats_radio_perf", "fieldset", drivers)
        # #loadPage("menu_node_stats_radio_history", "fieldset", drivers)    #this page, confirms the user wants to leave. Not sure how to handle that with selenium.
        # loadPage("menu_node_stats_arp_cache", "fieldset", drivers)
        # loadPage("menu_node_stats_mac_table", "fieldset", drivers)
    except Exception as e:
        sys.stdout.write("Exception " + str(e))
    finally:
        try:
            # logout(config.ipaddress, gambit, drivers)
            time.sleep(5)
        except Exception as e:
            time.sleep(1)
        quit(drivers)
        time.sleep(5)


            #8,9,10,11,12,13, 15, 16, 17, 19, 21, 22, 23, 24, 26, 28, 29, 30, 31, 32, 33


sleepTime = 1
i = 0
#for i in range(500):
while True:
    sys.stdout.write("Test number " + str(i))
    sys.stdout.flush()
    try:
        test()  #
        print " Done"
    #except EOFError, e:
    except Exception as e:
        print ": Got error " + str(e)
    time.sleep(sleepTime)
    i += 1

