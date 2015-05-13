import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.common.action_chains import ActionChains
import time
from optparse import OptionParser


def main():
    parser = OptionParser(usage="usage: %prog ipAddress browser (chrome, firefox, ie)")
    # parser.add_option("-c", "--chelp", help="Add arguments for IP Address for radio and target browser")
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("wrong number of arguments")

    ChassisClick()


class ChassisClick():
    def __init__(self):
        self.driver = Utils.create_driver(sys.argv[2])
        login_handler = LoginHandler(self.driver)
        login_handler.start()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'menu_node_equipment')))
        time.sleep(5)

        self.driver.switch_to_frame('frame_content')
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'ChassisViewWidget1_container')))

        elem = self.driver.find_element_by_xpath("//canvas")

        top_offset = 200
        # the following from chassis_8540.js
        # 'logo', 25, 20 + top_offset
        # 'chassis_fan', 25, 73 + top_offset
        # 'chassis_slot2', 139, 5 + top_offset
        # 'chassis_slot3', 355, 5 + top_offset
        # 'chassis_slot4', 571, 5 + top_offset
        # 'chassis_slot5', 787, 5 + top_offset

        # click on slot4
        action = ActionChains(self.driver).move_to_element_with_offset(elem, 571, 5 + top_offset).click()
        action.perform()

        # found id's by opening developer tools (F12), clicking on the object on the chassis and when the menu appears
        # looking through html until finding the <ul> that contains the list of menu items. Can search for "chassis_context_menu_list".
        # The id will change depending on which slot you plug the module in and whether or not there are modules / fan in
        # slots 1-3 (if you are looking at slot 4), so you'll have to look at your setup to find correct id
        item = self.driver.find_element_by_id('5')
        item.click()

        login_handler.end()


class Utils(object):
    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def create_driver(driver_name):
        if driver_name == "chrome":
            return webdriver.Chrome("C:\ChromeDriver\chromedriver.exe")
        elif driver_name == "firefox":
            return webdriver.Firefox()
        elif driver_name == "ie":
            return webdriver.Ie()
        else:
            raise Exception("Unknown driver " + driver_name)

    @classmethod
    def start_browser(cls, driver):
        cls.get_address(driver)
        cls.window_init(driver)

    @classmethod
    def get_address(cls, driver):
        if len(sys.argv) < 2:
            print("Address argument missing")
            sys.exit()
        address = "http://" + sys.argv[1]
        driver.get(address)

    @classmethod
    def window_init(cls, driver):
        driver.set_window_size(1200, 800)

    @classmethod
    def login(cls, driver, username, password):
        try:
            # find the login element and type in the username
            input_element = driver.find_element_by_id("username")
            input_element.send_keys(username)
            # find the password element and type in the password
            input_element = driver.find_element_by_id("password")
            input_element.send_keys(password)
            # submit the form
            input_element.submit()
        except:
            print("Login page not as expected. Exiting...")
            driver.quit()
        try:
            # we have to wait for the page to refresh, the last thing that seems to be updated is the title
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "layout_device_name")))
            print('Login Successful')
            time.sleep(5)
        except:
            print("Login unsuccessful")

    # logout, as too many sessions are not allowed. Broke something so this NOT WORKING
    def logout(self):
        try:
            self.driver.switch_to_default_content()
            self.click_element("top_menu_users")
            self.click_element("top_menu_logout")
            print("Successfully logged out")
            login_button = Utils.find_element("login")
            if not login_button is None:
                self.driver.quit()
        except:
            try:
                self.driver.find_element_by_name("Login")
                self.driver.quit()
            except:
                print("Logout unsuccessful. This may cause errors with max number of sessions")

    def click_element(self, element):
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, element)))
        self.driver.find_element(By.ID, element).click()

    def find_element(self, element):
        try:
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, element)))
            return self.driver.find_element(By.ID, element)
        except NoSuchElementException:
            return 'not found'


class LoginHandler(object):
    driver = None
    utils = None

    @classmethod
    def __init__(cls, driver):
        cls.utils = Utils(driver)
        cls.driver = driver

    @classmethod
    def login(cls):
        print('doing nothing, already logged from start()')

    @classmethod
    def logout(cls):
        print('normal logout')

    @classmethod
    def start(cls):
        cls.utils.start_browser(cls.driver)
        cls.utils.login(cls.driver, 'root', 'admin123')

    @classmethod
    def end(cls):
        cls.utils.logout()


if __name__ == "__main__":
    main()