from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import guiLib
import sys, time, os

usr = "root"
pw = "admin123"
timetup = time.localtime()
iso = time.strftime('%Y-%m-%d %H:%M:%S ', timetup)
print "=====", iso, "====="

driver = guiLib.createDriver(sys.argv[2])

guiLib.getAddress(driver)
guiLib.windowInit(driver)

guiLib.login(driver, usr, pw)

driver.find_element_by_id("menu_node_7_tree").click()
WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "menu_node_14_tree")))
driver.find_element(By.ID, "menu_node_14_tree").click()
WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "menu_node_14")))
driver.find_element(By.ID, "menu_node_14").click()
driver.find_element_by_id("menu_node_15").click()

driver.switch_to_frame('frame_content')

downloadBtn = driver.find_element_by_id("download").text
downloadButtonLen = len(downloadBtn)
assert downloadButtonLen > 0, ("Expected Download button text > 0 but was ", downloadButtonLen)

test = 'sends'
restoreBtn = driver.find_element_by_class_name(test).text
restoreBtnLen = len(restoreBtn)
assert restoreBtnLen > 0, ("Expected Restore button text > 0 but was ", restoreBtnLen)

time.sleep(2)
