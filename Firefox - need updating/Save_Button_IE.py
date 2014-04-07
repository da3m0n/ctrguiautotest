from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import guiLib
import sys, time

if len(sys.argv) < 2 :
    print"Address argument missing"
    sys.exit()

# Create a new instance of the IE driver
driver = webdriver.Ie()
address = "http://"+sys.argv[1]

driver.get(address)
guiLib.windowInit(driver)

guiLib.login(driver,"root","admin123")

try:
    savebutton = driver.find_element(By.ID, "top_menu_save")
    if savebutton.text == "Save":
        print "Success!! Save button exists!"
    else:
        print "Save button not as expected"
        print "Save button:", savebutton.text

finally:
    guiLib.logout(driver)