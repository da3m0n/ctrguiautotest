import sys, os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium import webdriver


class Utils(object):
    # def __init__(self):
        # resultFile =

    @staticmethod
    def createDriver(driverName):
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
        self.windowInit(driver)

    def loginToRadio(self, driver, loggedIn):
        if loggedIn:
            usr = "root"
            pw = "admin123"
            local_time = time.localtime()
            iso = time.strftime('%Y-%m-%d %H:%M:%S ', local_time)
            print "=====", iso, "====="

            self.getAddress(driver)
            self.windowInit(driver)

            self.login(driver, usr, pw)
        else:
            print('Already logged in')

    @classmethod
    def login(self, driver, username, password):
        try:
            # find the login element and type in the username
            inputElement = driver.find_element_by_name("Login")
            inputElement.send_keys(username)
            # find the password element and type in the password
            inputElement = driver.find_element_by_name("Password")
            inputElement.send_keys(password)
            # submit the form
            inputElement.submit()
        except:
            print "Login page not as expected. Exiting..."
            driver.quit()
        try:
            # we have to wait for the page to refresh, the last thing that seems to be updated is the title
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "layout_device_name")))
            print 'Login Successful'
            time.sleep(5)
        except:
            print "Login unsuccessful"

    #logout, as too many sessions are not allowed
    def logout(self, driver):
        try:
            #find the logout button
            self.click_element(driver, "top_menu_logout")
            print "Successfully logged out"
            driver.quit()
        except:
            try:
                #otherwise check whether already on the login page
                page1 = driver.find_element_by_name("Login")
            except:
                print "Logout unsuccessful. This may cause errors with max number of sessions"


    #initialise the window size so that all elements are visible
    @classmethod
    def windowInit(self, driver):
        driver.set_window_size(1080, 800)
        print "Window Resized"
        #handle = driver.window_handles

    #get the page from the address argument, eg. 192.168.11.11
    @classmethod
    def getAddress(self, driver):
        if len(sys.argv) < 2:
            print "Address argument missing"
            sys.exit()
        address = "http://" + sys.argv[1]
        print "Getting address:", address
        #get page
        driver.get(address)

    #Get the help window
    def getHelp(self, driver):
        help = driver.find_element(By.ID, 'top_menu_help')
        help.click()

        time.sleep(2)
        #check that two windows exist
        handle = driver.window_handles
        if len(handle) != 2:
            print "Incorrect number of windows found"
            print handle
            sys.exit()
        time.sleep(5)
        try:
            driver.switch_to_window(handle[1])
            print "changing to help window"
        except:
            print "Unable to change to the help window"
            sys.exit()
        driver.switch_to_frame("body")
        popup = driver.find_element(By.XPATH, "//body/h1").text
        print "Popup:", popup
        popup = popup.upper()
        return popup

    # need to complete this method
    def insertJS(self, driver, elem, str):
        driver.execute_script("document.getElementById('SystemInformationWidget1_TW_0_1_renderer').innerHTML=\"\";")
        return None

    @staticmethod
    def click_element(driver, element):
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, element)))
        driver.find_element(By.ID, element).click()

    @staticmethod
    def delete_existing_logfile():
        if os.path.isfile('errors.log'):
            os.remove('errors.log')
        else:
            print('No existing error.log file.')