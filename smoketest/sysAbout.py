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
# driver.switch_to_default_content()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "menu_node_7_tree")))

driver.find_element_by_id("menu_node_7_tree").click()
time.sleep(2)
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "menu_node_10")))
driver.find_element_by_id("menu_node_10").click()
driver.switch_to_frame("frame_content")

try:
    about = driver.find_element(By.XPATH, "//body/fieldset/legend").text
    assert about == "About", ("Expected About but got ", about)

    title = 'Aviat Networks Converged Transport Router'
    webTitle = driver.find_element_by_xpath('//body/fieldset/div/div/h3').text
    assert title == webTitle, ('Expected ', title, ' but got ', webTitle)

    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'licenses')))
    time.sleep(2)
    licenses = driver.find_element_by_id('licenses')
    licensesLen = len(licenses.text)
    assert licensesLen > 0, ('Expected Licenses length to be > 0 but was ', licensesLen)
except "Element Not Found Exception":
    print "About element not found."

time.sleep(2)