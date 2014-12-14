import sys, os
from smoketest.mylib.utils import Utils


class LoginHandler(object):
    def __init__(self, driver):
        self.utils = Utils(driver, None)
        self.driver = driver

    def login(self):
        print('doing nothing, already logged from start()')

    def logout(self):
        print('normal logout')

    def start(self):
        self.utils.startBrowser(self.driver)
        self.utils.login(self.driver, 'root', 'admin123')

    def end(self):
        # self.driver.switch_to_default_content()
        self.utils.logout(self.driver)