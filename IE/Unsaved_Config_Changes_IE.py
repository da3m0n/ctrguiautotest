from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import sys, time

if len(sys.argv) < 2 :
    print"Address argument missing"
    sys.exit()

# Create a new instance of the Firefox driver
driver = webdriver.Ie()
address = "http://"+sys.argv[1]

# get the login page
driver.get(address)

driver.maximize_window()

# find the username element
inputElement = driver.find_element_by_name("Login")
inputElement.send_keys("root")

# find the password element
inputElement = driver.find_element_by_name("Password")
inputElement.send_keys("admin123")

inputElement.submit()

try:
    # we have to wait for the page to refresh, the last thing that seems to be updated is the title
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "layout_device_name")))

    print 'Login Successful'

except:
    print "Login unsuccessful"
    driver.quit()

driver.set_window_size(1080,800)
print"Window Resized"

handle = driver.window_handles

try:
    time.sleep(5)
    config = driver.find_element(By.ID, "menu_node_6_toggle").click()

#add in some more clicks to change a config

 #   warning = driver.find_element(By.CLASS_NAME, "activity_status_warning").text
 #   if warning == "Unsaved configuration changes":
 #       print "Correct warning in place"
 #   else:
 #       print "No warning about unsaved config changes"""
finally:
    try:
        driver.switch_to_window(handle[0])
        print "changing to main window"
    except:
        print "unable to return to the main window"
        sys.exit()
    try:
        logout = driver.find_element(By.ID, "top_menu_logout")
        logout.click()
        print "Successfully logged out"
    except:
        print "Logout unsuccessful. This may cause errors with max number of sessions"
    driver.quit()