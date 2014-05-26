import sys
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

import os
from smoketest.utils import guiLib


usr = "root"
pw = "admin123"
timetup = time.localtime()
iso = time.strftime('%Y-%m-%d %H:%M:%S ', timetup)
print("=====", iso, "=====")

# Create a new instance of the IE driver
# driver = webdriver.Firefox()
# os.system("wmic path win32_networkadapter where index=7 call enable")
# os.system("wmic path win32_networkadapter where index=7 call enable")

driver = guiLib.createDriver(sys.argv[2])

guiLib.getAddress(driver)
guiLib.windowInit(driver)

guiLib.login(driver, usr, pw)

try:
    print("------- Disconnection Network Adapter -------")
    os.system("wmic path win32_networkadapter where index=7 call disable")
    print("---------------------------------------------")
    # time.sleep(15)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "ui-dialog-title")))
    status = driver.find_element_by_class_name("ui-dialog-title").text

    assert status == "Connection Error"

    # if status == "Connection Error":
    #     print("Connection Error Detected")
    #     # assert status == "Connection Error1"
    #     # raise Exception("Status is incorrect")
    #     print("---------------------------------------------")
    # else:
    #     print("Connection Error Not Detected")
    #     print(status)
    #     print("---------------------------------------------")

    print "------- Connecting Network Adapter -------"
    os.system("wmic path win32_networkadapter where index=7 call enable")
    print "------------------------------------------"

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "up")))

    assert driver.find_element_by_class_name("up")
    # if status == "":
    #     print("Reconnection succeeded")
    # else:
    #     print("Reconnection did not succeed")
    # print("------ Status ------")
    # print(status)
    # print("--------------------")
except:
    print("-----------------------------------")
    print("Exception encountered, enabling network connection")
    os.system("wmic path win32_networkadapter where index=7 call enable")
    print("-----------------------------------")
    # guiLib.logout(driver)

finally:
    guiLib.logout(driver)



# try:
#     status = driver.find_element(By.ID, "top_menu_activites").text
#     if status == "Connected to device":
#         print "First header verified"
#     else:
#         print "First header not verified"
#         print status
#     time.sleep(10)
#     print "-----------------------------------"
#     # os.system("wmic path win32_networkadapter where index=7 call disable")
#     print "-----------------------------------"
#     time.sleep(15)
#     driver.find_element(By.CLASS_NAME, "top_menu_dropdown_arrow")
#     WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.CLASS_NAME, "activity_status_list"))
#     status = driver.find_element(By.CLASS_NAME, "activity_status_list_item")
#
#     driver.switch_to_default_content()
#     selectBox = driver.find_element(By.CLASS_NAME, "activity_status_list")
#     options = [x for x in selectBox.find_element_by_class_name("activity_status_list_item").text]
#     for elem in options:
#         print("eleM: ", elem.text)
#     print("status: ", status)
#     if status == "Connection to device lost":
#         print "Second header verified"
#     else:
#         print "Second header not verified"
#         print status
#     print "-----------------------------------"
#     os.system("wmic path win32_networkadapter where index=7 call enable")
#     print "-----------------------------------"
#     time.sleep(20)
#     driver.find_element(By.CLASS_NAME, "top_menu_dropdown_arrow").click()
#     WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.CLASS_NAME, "activity_status_list"))
#     status = driver.find_element(By.CLASS_NAME, "activity_status_list").text
#     if "Connecting to device..." in status:
#         print "Third header verified"
#     else:
#         print "Third header not verified"
#         print status
#     driver.find_element(By.CLASS_NAME, "top_menu_dropdown_arrow").click()
#     time.sleep(60)
#     WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.CLASS_NAME, "activity_status_list"))
#     status = driver.find_element(By.CLASS_NAME, "activity_status_list").text
#     if "Connected to device" in status:
#         print "Fourth header verified"
#     else:
#         print "Fourth header not verified"
#         print status
#     print "PASS"
# except:
#     print "-----------------------------------"
#     os.system("wmic path win32_networkadapter where index=7 call enable")
#     print "-----------------------------------"
#     guiLib.logout(driver)
#
# finally:
#     guiLib.logout(driver)
