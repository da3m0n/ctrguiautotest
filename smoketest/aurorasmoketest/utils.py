import sys, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium import webdriver


class Utils(object):
    def __init__(self, driver):
        rt = None
        self.driver = driver

    @staticmethod
    def create_driver(driverName):
        if driverName == "chrome":
            return webdriver.Chrome("C:\ChromeDriver\chromedriver.exe")
        elif driverName == "firefox":
            return webdriver.Firefox()
        elif driverName == "ie":
            return webdriver.Ie()
        else:
            raise Exception("Unknown driver " + driverName)

    def startBrowser(self, driver):
        self.getAddress(driver)
        driver.set_window_size(1200, 800)

    @classmethod
    def login(cls, driver, username, password, counter):
        try:
            # find the login element and type in the username
            inputElement = driver.find_element_by_id("username")
            inputElement.send_keys(username)
            # find the password element and type in the password
            inputElement = driver.find_element_by_id("password")
            inputElement.send_keys(password)
            # submit the form
            inputElement.submit()
        except:
            print("Login page not as expected. Exiting...")
            driver.quit()
        try:
            # we have to wait for the page to refresh, the last thing that seems to be updated is the title
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "layout_device_name")))
            print "Login Successful - #", counter
            time.sleep(5)
        except:
            print("Login unsuccessful")

    #logout, as too many sessions are not allowed
    def logout(self, driver):
        try:
		    driver.get("http://" + sys.argv[1] + "/logout")
		#
            #find the logout button
        #    self.click_element("top_menu_users")
        #    self.click_element("top_menu_logout")
        #    print("Successfully logged out")
        #    login_button = Utils.find_element('login')
        #    if not login_button is None:
        #        driver.quit()
        except:
            print("Logout button not found, must be logged out...hopefully.")
        finally:
            driver.quit()

    #get the page from the address argument, eg. 192.168.11.11
    @classmethod
    def getAddress(self, driver):
        if len(sys.argv) < 2:
            print("Address argument missing")
            sys.exit()
        address = "http://" + sys.argv[1]
        #get page
        driver.get(address)

    def click_element(self, element):
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, element)))
        self.driver.find_element(By.ID, element).click()
