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
WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "menu_node_13")))
driver.find_element_by_id("menu_node_13").click()

driver.switch_to_frame("frame_content")
WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "PowerConfigWidget1_TW_table")))
table = driver.find_element_by_id("PowerConfigWidget1_TW_table")

headers = table.find_elements_by_tag_name('th')
setHeaders = ['Slot', 'Power Expected', 'Voltage', 'Current', 'Temperature', '']

count = 0
for head in headers:
    assert head.text == setHeaders[count], ('Expected ', setHeaders[count], ' but got ', head.text)
    count += 1

# driver.execute_script("document.getElementById('PowerConfigWidget1_TW_304087040_slot').innerHTML=\"\";")

slot = table.find_element_by_id("PowerConfigWidget1_TW_304087040_slot").text
slotLen = len(slot)
assert slotLen > 0, ("Expected slot length to be > 0 but was ", slotLen)
time.sleep(2)
