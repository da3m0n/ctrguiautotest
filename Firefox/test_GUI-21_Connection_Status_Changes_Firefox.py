from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import guiLib
import sys, time, os
from subprocess import call

usr = "root"
pw = "admin123"

# Create a new instance of the IE driver
driver = guiLib.createDriver(sys.argv[2])

guiLib.getAddress(driver)
guiLib.windowInit(driver)

guiLib.login(driver, usr, pw)

try:
    status = driver.find_element(By.ID, "top_menu_activites").text
    if status == "Connected to device":
        print "First header verified"
    else:
        print "First header not verified"
        print status
    time.sleep(10)
    print "-----------------------------------"
    os.system("wmic path win32_networkadapter where index=7 call disable")
    print "-----------------------------------"
    time.sleep(15)
    driver.find_element(By.CLASS_NAME, "top_menu_dropdown_arrow").click()
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.CLASS_NAME, "activity_status_list"))
    status = driver.find_element(By.CLASS_NAME, "activity_status_list_item").text
    if status == "Connection to device lost":
        print "Second header verified"
    else:
        print "Second header not verified"
        print status
    print "-----------------------------------"
    os.system("wmic path win32_networkadapter where index=7 call enable")
    print "-----------------------------------"
    time.sleep(20)
    driver.find_element(By.CLASS_NAME, "top_menu_dropdown_arrow").click()
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.CLASS_NAME, "activity_status_list"))
    status = driver.find_element(By.CLASS_NAME, "activity_status_list").text
    if "Connecting to device..." in status:
        print "Third header verified"
    else:
        print "Third header not verified"
        print status
    driver.find_element(By.CLASS_NAME, "top_menu_dropdown_arrow").click()
    time.sleep(60)
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.CLASS_NAME, "activity_status_list"))
    status = driver.find_element(By.CLASS_NAME, "activity_status_list").text
    if "Connected to device" in status:
        print "Fourth header verified"
    else:
        print "Fourth header not verified"
        print status
finally:
    guiLib.logout(driver)
