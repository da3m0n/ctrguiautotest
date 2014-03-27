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

try:
    guiLib.getAddress(driver)
    guiLib.windowInit(driver)

    z = 0
    while z!=2:
        guiLib.login(driver,usr, pw)
        time.sleep(15)
        driver.find_element(By.ID, "menu_node_6_toggle").click()
        time.sleep(5)
        driver.find_element(By.ID, "menu_node_11_toggle").click()
        time.sleep(5)
        driver.find_element(By.ID, "menu_node_13").click()
        time.sleep(10)
        status = driver.find_element(By.ID, "top_menu_activites").text
        while status != "Software: Rolling back":
            driver.switch_to_frame("frame_content")
            button = driver.find_element(By.TAG_NAME, "button")
            button.click()
            driver.switch_to_default_content()
            WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.TAG_NAME, "button"))
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for item in buttons:
                if item.text == "Yes":
                    item.click()
                    time.sleep(5)
                    print"rolling back software..."
                    break
            status = driver.find_element(By.ID, "top_menu_activites").text
        print"waiting for login page"
        time.sleep(200)
        driver.refresh()
        WebDriverWait(driver, 500).until(EC.title_contains("Login"))
        z+=1

    print "Software rollback and restore successful"
    print "PASS"
finally:
    guiLib.logout(driver)
