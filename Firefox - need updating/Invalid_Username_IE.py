from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

from smoketest.utils import guiLib


usr = "r"
pw = "admin123"

# Create a new instance of the IE driver
driver = webdriver.Ie()

guiLib.getAddress(driver)
guiLib.windowInit(driver)

guiLib.login(driver,usr, pw)

try:
    # wait until the expected login error is found on the page after refreshing
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login_error")))


    print 'Success! Error message correctly displayed for incorrect username'

finally:
    guiLib.logout(driver)