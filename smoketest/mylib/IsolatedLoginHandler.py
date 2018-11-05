from smoketest.mylib.utils import Utils
import os


class IsolatedLoginHandler(object):
    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(driver)

    def login(self):
        # self.utils.delete_existing_logfile()
        self.utils.startBrowser(self.driver)
        self.utils.login(self.driver, 'root', 'admin123')

    def logout(self):
        self.driver.switch_to_default_content()
        self.utils.logout(self.driver)
