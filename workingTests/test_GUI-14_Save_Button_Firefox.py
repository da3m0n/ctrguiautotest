import sys
import time

from selenium.webdriver.common.by import By

from smoketest.utils import guiLib


usr = "root"
pw = "admin123"
timetup = time.localtime()
iso = time.strftime('%Y-%m-%d %H:%M:%S ', timetup)
print "=====", iso, "====="

# Create a new instance of the FF driver
driver = guiLib.createDriver(sys.argv[2])

guiLib.getAddress(driver)
guiLib.windowInit(driver)

guiLib.login(driver,usr, pw)

try:
    savebutton = driver.find_element(By.ID, "top_menu_save")
    if savebutton.text == "Save":
        print "Success!! Save button exists!"
    else:
        print "Save button not as expected"
        print "Save button:", savebutton.text
    print "PASS"

finally:
    guiLib.logout(driver)
