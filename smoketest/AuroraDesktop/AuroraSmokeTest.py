from utils import Utils


class AuroraSmokeTest():
    def __init__(self, driver):
        self.driver = driver
        self.gui_lib = Utils(driver)

    def navigate_to_screen(self, screen_name):
        self.__navigate_to_location(screen_name)

    def __navigate_to_location(self, screen_name):
        self.driver.switch_to_default_content()
        self.gui_lib.click_element(screen_name)