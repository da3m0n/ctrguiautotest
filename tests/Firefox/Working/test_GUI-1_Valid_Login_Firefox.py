import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from smoketest.utils import guiLib


usr = "root"
pw = "admin123"
timetup = time.localtime()
iso = time.strftime('%Y-%m-%d %H:%M:%S ', timetup)
print "=====", iso, "====="

# Create a new instance of the IE driver
# driver = webdriver.Firefox()
driver = webdriver.Chrome("C:\chromedriver.exe")

guiLib.getAddress(driver)
guiLib.windowInit(driver)

guiLib.login(driver, usr, pw)

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