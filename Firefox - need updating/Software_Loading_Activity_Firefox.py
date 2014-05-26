import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

from smoketest.utils import guiLib


usr = "root"
pw = "admin123"

# Create a new instance of the IE driver
driver = webdriver.Ie()

guiLib.getAddress(driver)
guiLib.windowInit(driver)

z = 0
while z!=2:
    guiLib.login(driver,usr, pw)
    time.sleep(15)
    driver.find_element(By.ID, "menu_node_6_tree").click()
    time.sleep(5)
    driver.find_element(By.ID, "menu_node_11_tree").click()
    time.sleep(5)
    driver.find_element(By.ID, "menu_node_13").click()
    time.sleep(10)
    status = driver.find_element(By.ID, "top_menu_activites").text
    while status != "Software: Rolling back":
        print status
        driver.switch_to_frame("frame_content")
        button = driver.find_element(By.TAG_NAME, "button")
        print button.text
        button.click()
        print ""
        driver.switch_to_default_content()
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.TAG_NAME, "button"))
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for item in buttons:
            print item.text
            if item.text == "Yes":
                item.click()
                time.sleep(5)
                print"rolling back software..."
                break
        status = driver.find_element(By.ID, "top_menu_activites").text
    print"waiting for login page"
    
    WebDriverWait(driver, 500).until(EC.title_contains("Login"))
    z+=1
    


guiLib.logout(driver)