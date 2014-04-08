from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# import guiLib
import sys
# from smoketest.mylib import IsolatedLoginHandler
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler

from smoketest.mylib.utils import Utils


def main():
    date_time = DateTime(IsolatedLoginHandler())
    date_time.run_date_time(Utils.createDriver(sys.argv[2]))
    print("Inside dateTime().main()")


class DateTime(object):
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def run_date_time(self, driver):
        gui_lib = Utils()

        self.login_manager.login(driver)

        driver.switch_to_default_content()
        driver.find_element_by_id("menu_node_7_tree").click()
        gui_lib.click_element(driver, "menu_node_9")
        driver.switch_to_frame("frame_content")

        table = driver.find_element_by_id("DateTimeWidget1_TW_table")
        WebDriverWait(table, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "TableWidget_verticalTableHeading")))

        headers = table.find_elements_by_class_name('TableWidget_verticalTableHeading')
        set_headers = ['', 'Clock Source', 'Date', 'Time', 'Timezone']

        errors = open('errors.log', 'a')
        errors.write('======== Date / Time\n')
        errors.write('________ FAILURES\n')
        count = 0
        for head in headers:
            # assert head.text == set_headers[count], ('Expected ', set_headers[count], ' but got ', head.text)
            if head.text != set_headers[count]:
                errors.write('we have a problem\n')
                break
            count += 1

            # time = table.find_element_by_class_name('renderer_datetime_input')
            # print(time.text)
            #
            # timeZone = table.find_element_by_id('DateTimeWidget1_TW_3_1')
            # print(timeZone)
        errors.write('======== End Date / Time\n\n')
        errors.close()
        self.login_manager.logout(driver)

if __name__ == "__main__":
    main()