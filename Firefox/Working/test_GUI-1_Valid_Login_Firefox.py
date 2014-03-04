from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import guiLib
import sys, time, os

usr = "root"
pw = "admin123"
timetup = time.localtime()
iso = time.strftime('%Y-%m-%d %H:%M:%S ', timetup)
print "=====", iso, "====="

# Create a new instance of the IE driver
driver = webdriver.Firefox()

guiLib.getAddress(driver)
guiLib.windowInit(driver)

guiLib.login(driver,usr, pw)

try:
    user = driver.find_element(By.ID, 'top_menu_users').text
    print("User", user)
    if user == usr:
        print "Username verified in top menu"
    else:
        print "Particular user not found"
        raise Exception("user not found")
    print "PASS"
except:
    print"no users found"

finally:
    guiLib.logout(driver)