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
    time.sleep(15)
    driver.find_element(By.ID, "menu_node_6_toggle").click()
    time.sleep(5)
    driver.find_element(By.ID, "menu_node_7").click()
    time.sleep(5)
    ip = driver.find_element(By.ID, "status_bar_device_name").text.split()
    print "IP:", ip[0]
    driver.switch_to_frame("frame_content")
    time.sleep(20)
    name = driver.find_element(By.XPATH, "//*[@id='SystemInformationWidget1_TW_3_1_renderer']/input")
    print "Name:",name.get_attribute("value")
    site = driver.find_element(By.XPATH, "//*[@id='SystemInformationWidget1_TW_6_1_renderer']/input")
    print "Site:", site.get_attribute("value")
    name.clear()
    name.send_keys("Dory")
    site.clear()
    site.send_keys("42 Wallaby Way")
    assert name.get_attribute("value") == "Dory"
    print "Name:",name.get_attribute("value")
    assert site.get_attribute("value") == "42 Wallaby Way"
    print "Site:", site.get_attribute("value")
    print "Name and site information verified"
    print "PASS"

except:
    print "Failed to find info, page not as expected"

finally:
    driver.switch_to_default_content()
    guiLib.logout(driver)
