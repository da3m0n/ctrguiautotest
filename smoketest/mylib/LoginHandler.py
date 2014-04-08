import sys, os
from smoketest.mylib.utils import Utils


class LoginHandler(object):
    def __init__(self):
        self.utils = Utils()

    def login(self, driver):
        print('doing nothing, already logged from start()')

    def logout(self, driver):
        print('normal logout')

    def start(self, driver):
        self.utils.startBrowser(driver)
        self.utils.login(driver, 'root', 'admin123')

    def end(self, driver):
        driver.switch_to_default_content()
        self.utils.logout(driver)