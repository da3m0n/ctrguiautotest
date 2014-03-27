from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import guiLib, cliLib
import sys, time, os
import telnetlib

usr = "user!)"
pw = "admin123"
timetup = time.localtime()
iso = time.strftime('%Y-%m-%d %H:%M:%S ', timetup)
print "=====", iso, "====="
driver = None
tn = telnetlib.Telnet(sys.argv[1])

try:
    if not cliLib.ctrLogin(tn, "root", "admin123"):
        print "User name or Password incorrect"
    else:
        print "Logged In"
        original = cliLib.getPasswordRestrictions(tn)
        print "Original:", original
        cliLib.clearPasswordRestrictions(tn)
        cliLib.newUser(tn, usr, pw)

    # Create a new instance of the IE driver
    driver = webdriver.Firefox()

    guiLib.getAddress(driver)
    guiLib.windowInit(driver)

    guiLib.login(driver,usr, pw)

    user = driver.find_element(By.ID, 'top_menu_users').text
    if user == usr:
        print "Username verified in top menu"
    else:
        print "Particular user not found"
        raise Exception("User not found")
    print "PASS"

finally:
    cliLib.deleteUser(tn, usr)
    cliLib.resetPasswordRestrictions(tn, original)
    assert cliLib.getPasswordRestrictions(tn) == original
    tn.close()
    if driver!= None:
        guiLib.logout(driver)