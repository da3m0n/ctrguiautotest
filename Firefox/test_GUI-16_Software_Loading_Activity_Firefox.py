from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
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
driver = guiLib.createDriver(sys.argv[2])

try:
    guiLib.getAddress(driver)
    guiLib.windowInit(driver)

    # z = 0
    # while z != 2:
    guiLib.login(driver, usr, pw)
    time.sleep(10)
    driver.find_element(By.ID, "menu_node_7_tree").click()
    time.sleep(5)
    driver.find_element(By.ID, "menu_node_14_tree").click()
    time.sleep(5)
    driver.find_element(By.ID, "menu_node_16").click()
    time.sleep(5)
    status = driver.find_element(By.ID, "top_menu_activites").text
    # while status != "Software: Rolling back":

    driver.switch_to_frame("frame_content")
    button = driver.find_element(By.ID, "SoftwareLoadingStatusWidget1_rollback")
    button.click()

    driver.switch_to_default_content()
    # driver.find_element_by_class_name("ui-dialog-title")
    # text = driver.find_element_by_class_name("ui-button-text").text
    buttons = driver.find_elements(By.CLASS_NAME, "ui-button-text")
    for button in buttons:
        print("Button name", button.text)
        if button.text == "No":
            print("Decline rollback")
            button.click()
            time.sleep(5)


    # driver.find_element(By.ID, "ui-dialog")
    # confirmButton = driver.find_element(By.CLASS_NAME, "ui-button-text")
    # confirmButton.click()
#     driver.switch_to_default_content()
#     WebDriverWait(driver, 10).until(lambda driver2: driver2.find_element(By.TAG_NAME, "button"))
#     buttons = driver.find_elements(By.TAG_NAME, "button")
#     for item in buttons:
#         if item.text == "Yes":
#             item.click()
#             time.sleep(5  )
#             print"rolling back software..."
#             break
#     status = driver.find_element(By.ID, "top_menu_activites").text
# print"waiting for login page"
# time.sleep(200)
# driver.refresh()
# WebDriverWait(driver, 500).until(EC.title_contains("Login"))
# z += 1

    print "Software rollback and restore successful"
    print "PASS"
finally:
    guiLib.logout(driver)
