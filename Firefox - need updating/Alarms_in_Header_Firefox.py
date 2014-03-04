from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import sys, time, os
from lib import CSRTest
from lib.device.testrig_win import TestRig

def main(testrig):
    usr = "root"
    pw = "admin123"
    mainDevice = testrig.getMainDevice()
    alarms = mainDevice.getAlarms()
    alarmName = alarms.ALARM_NAME
    
    print alarmName
    
    driver = webdriver.Ie()
    address = "http://"+sys.argv[1]
    
    guiLib.getAddress(driver)
    guiLib.windowInit(driver)
    
    guiLib.login(driver,usr, pw)
    
    handle = driver.window_handles
    try:
        alarms.initAlarms(testrig)
        #enable logging of alarm
        alarms.enableLogging(alarmName)
        time.sleep(2)
        alarm = driver.find_element(By.ID, "alarm_status_container").text
        alarm = alarm.split()
        print "Critical Alarms:", alarm[0]
        print "Major Alarms:", alarm[1]
        #raise alarm
        alarms.raiseAlarm()
        alarm = driver.find_element(By.ID, "alarm_status_container").text
        alarm = alarm.split()
        print "Critical Alarms:", alarm[0]
        print "Major Alarms:", alarm[1]
    
    finally:
        driver.switch_to_window(handle[0])
        logout  = driver.find_element(By.ID, "top_menu_logout")
        logout.click()
        print "Successfully logged out"
        driver.quit()
    
if __name__ == "__main__":
    main("http:\\192.168.11.33")