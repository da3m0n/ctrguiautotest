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

driver.switch_to_default_content()
driver.find_element_by_id("menu_node_7_tree").click()
driver.find_element_by_id("menu_node_8").click()
driver.switch_to_frame("frame_content")
table = driver.find_element_by_id("SystemInformationWidget1_TW_table")
WebDriverWait(table, 10).until(EC.presence_of_element_located((By.ID, "SystemInformationWidget1_TW_0")))

headers = table.find_elements_by_tag_name('th')
setHeaders = ['', 'Hardware Version', 'Software Version', 'Firmware Version', 'Node Name', 'Switch MAC', 'Contact',
              'Location']

count = 0
for head in headers:
    assert head.text == setHeaders[count], ('Expected ', setHeaders[count], ' but got ', head.text)
    count += 1

hwVersion = table.find_element_by_id('SystemInformationWidget1_TW_0_1')
# driver.execute_script("document.getElementById('SystemInformationWidget1_TW_0_1_renderer').innerHTML=\"\";")
hwVersionLen = len(hwVersion.text)
assert hwVersionLen > 0, ('Expected length of Hardware Version to be greater than zero but was ', hwVersionLen)

swVersion = table.find_element_by_id('SystemInformationWidget1_TW_1_1')
swVersionLen = len(swVersion.text)
assert swVersionLen > 0, ('Expected length of Software Version to be greater than zero but was ', swVersionLen)

firmVersion = table.find_element_by_id('SystemInformationWidget1_TW_2_1')
firmVersionLen = len(firmVersion.text)
assert firmVersionLen > 0, ('Expected length of Firmware Version to be greater than zero but was ', firmVersionLen)

time.sleep(2)
