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

    def startBrowser(self, driver, port):
        self.getAddress(driver, port)
        driver.set_window_size(1200, 800)

    @classmethod
    def getAddress(self, driver, port):
        if len(sys.argv) < 2:
            print("Address argument missing")
            sys.exit()
        address = "http://" + sys.argv[1] + ":" + port
        #get page
        driver.get(address)

    def click_element(self, element):
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, element)))
        self.driver.find_element(By.ID, element).click()
