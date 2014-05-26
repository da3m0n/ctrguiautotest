import sys
import time

from selenium.webdriver.common.by import By

from smoketest.utils import guiLib


usr = "root"
pw = "admin123"

# Create a new instance of the FF driver
driver = guiLib.createDriver(sys.argv[2])

guiLib.getAddress(driver)
guiLib.windowInit(driver)

guiLib.login(driver, usr, pw)

handle = driver.window_handles

try:
    print driver.title

    page = driver.find_element(By.ID, "menu_node_1").text
    print "First Page:", page
    driver.find_element(By.ID, 'top_menu_help').click()
    # help.click()

    time.sleep(2)
    handle = driver.window_handles
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
    page = page.upper()
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
    help2.click()
    help2 = driver.find_element(By.ID, "menu_node_3")
    print "Second Page:", help2.text

    time.sleep(5)
    page = help2.text
    driver.switch_to_default_content()
    driver.find_element(By.ID, 'top_menu_help').click()
    time.sleep(2)
    handle = driver.window_handles
    
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
