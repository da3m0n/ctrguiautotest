from smoketest.mylib.utils import Utils
import os


class IsolatedLoginHandler(object):
    def __init__(self):
        self.utils = Utils()

    def login(self, driver):
        # self.utils.delete_existing_logfile()
        self.utils.startBrowser(driver)
        self.utils.login(driver, 'root', 'admin123')

    def logout(self, driver):
        driver.switch_to_default_content()
        self.utils.logout(driver)
