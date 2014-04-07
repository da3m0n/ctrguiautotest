import sys
from smoketest.mylib.utils import Utils


class LoginHandler(object):
    def __init__(self):
        self.utils = Utils()

    def login(self, driver):
        print('normal login, doing nothing, already logged from start()')

    def logout(self, driver):
        print('normal logout')

    def start(self, driver):
        print('start(), logging in for all tests')
        self.utils.startBrowser(driver)
        self.utils.login(driver, 'root', 'admin123')


    def end(self, driver):
        print('end all tests, log out and close browser')
        driver.switch_to_default_content()
        self.utils.logout(driver)