from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# import guiLib
import sys

from smoketest.mylib.utils import Utils


def main():
    print('calling dateTime')


class DateTime(object):
    def __init__(self, loggedIn):
        self.loggedIn = loggedIn

    def runDateTime(self):
        # driver = guiLib.createDriver(sys.argv[2])

        print(Utils)
        guiLib = Utils(True)
        driver = guiLib.createDriver(sys.argv[2])

        guiLib.loginToRadio(driver, True)

        driver.switch_to_default_content()
        driver.find_element_by_id("menu_node_7_tree").click()
        guiLib.click_element(driver, "menu_node_9")
        driver.switch_to_frame("frame_content")

        table = driver.find_element_by_id("DateTimeWidget1_TW_table")
        WebDriverWait(table, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "TableWidget_verticalTableHeading")))

        headers = table.find_elements_by_class_name('TableWidget_verticalTableHeading')
        setHeaders = ['Clock Source', 'Date', 'Time', 'Timezone']

        count = 0
        for head in headers:
            assert head.text == setHeaders[count], ('Expected ', setHeaders[count], ' but got ', head.text)
            count += 1

            # time = table.find_element_by_class_name('renderer_datetime_input')
            # print(time.text)
            #
            # timeZone = table.find_element_by_id('DateTimeWidget1_TW_3_1')
            # print(timeZone)


if __name__ == "__main__":
    dateTime = DateTime(True)
    dateTime.runDateTime()