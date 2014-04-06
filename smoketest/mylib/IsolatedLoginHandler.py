from smoketest.mylib.utils import Utils


class IsolatedLoginHandler(object):
    def __init__(self):
        self.utils = Utils()

    def login(self, driver):
        print('isolated login')
        self.utils.startBrowser(driver)
        self.utils.login(driver, 'root', 'admin123')

    def logout(self, driver):
        print('isolated logout')
        self.utils.logout(driver)
