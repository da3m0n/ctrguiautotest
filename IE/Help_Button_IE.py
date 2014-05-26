import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from smoketest.utils import guiLib


usr = "root"
pw = "admin123"


# Create a new instance of the IE driver
driver = webdriver.Ie()

guiLib.getAddress(driver)
guiLib.windowInit(driver)

guiLib.login(driver,usr, pw)

handle = driver.window_handles

try:
    print driver.title

    #driver.switch_to_frame("frame_content")
    page = driver.find_element_by_tag_name('a').text
    print "First Page:", page
    help = driver.find_element(By.ID, 'top_menu_help')
    help.click()

    time.sleep(2)
    handle  = driver.window_handles
    if len(handle) != 2:
        print "Incorrect number of windows found"
        print handle
        sys.exit()
    time.sleep(5)
    try:
        driver.switch_to_window(handle[1])
        print "changing to help window"
    except:
        print "unable to change to the help window"
        sys.exit()
    time.sleep(10)
    driver.switch_to_frame("body")
    popup = driver.find_element(By.XPATH, "//body/h1").text
    print "Popup:", popup
    popup = popup.upper()
    if page in popup or popup in page:
        print "Success! Help relevant to page!"
    else:
        print "Help not relevant to page"
    try:
        driver.switch_to_window(handle[0])
        print "changing to main window"
    except:
        print "unable to return to the main window"
    help2 = driver.find_element(By.ID, "menu_node_3")
    if driver.find_element_by_tag_name('a').text == page:
            help2.click()
    else:
        print "error clicking"

    print "Second Page:", help2.text
    help2.click()

    time.sleep(5)
    page = help2.text
    driver.switch_to_default_content()
    help = driver.find_element(By.ID, 'top_menu_help').click()
    time.sleep(2)
    handle  = driver.window_handles
    
    num = 0
    if len(handle) == 2: 
        num = 1
    elif len(handle) == 3:
        num = 2
    else:
        print "Incorrect number of windows found"
        print handle
        sys.exit()

    try:
        driver.switch_to_window(handle[num])
        print "changing to help window"
    except:
        print "unable to change to the help window"
        sys.exit()
    time.sleep(10)
    driver.switch_to_frame("body")
    popup = driver.find_element(By.XPATH, "//body/h1").text
    print "Popup:", popup
    if page in popup or popup in page:
        print "Success! Help relevant to page!"
    else:
        print "Help not relevant to page"


finally:
    try:
        driver.switch_to_window(handle[0])
        print "changing to main window"
    except:
        print "unable to return to the main window"
        sys.exit()
    guiLib.logout(driver)