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
driver.find_element_by_id("menu_node_9").click()
driver.switch_to_frame("frame_content")

table = driver.find_element_by_id("DateTimeWidget1_TW_table")
WebDriverWait(table, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "TableWidget_verticalTableHeading")))

headers = table.find_elements_by_class_name('TableWidget_verticalTableHeading')
setHeaders = ['Clock Source', 'Date',  'Time', 'Timezone']

count = 0
for head in headers:
    assert head.text == setHeaders[count], ('Expected ', setHeaders[count], ' but got ', head.text)
    count += 1

# time = table.find_element_by_class_name('renderer_datetime_input')
# print(time.text)
#
# timeZone = table.find_element_by_id('DateTimeWidget1_TW_3_1')
# print(timeZone)