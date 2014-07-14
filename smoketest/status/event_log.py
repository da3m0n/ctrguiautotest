from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.IsolatedLoginHandler import IsolatedLoginHandler
from smoketest.mylib.utils import Utils
import sys


def main():
    driver = Utils.create_driver(sys.argv[2])
    log_dir = Utils.log_dir()
    Utils.delete_existing_logfile(log_dir)
    test_log = TestLog(EventLog, log_dir)
    # create instance of class here and then  run method of class 
    event_log = EventLog(IsolatedLoginHandler())
    event_log.run_event_log(driver, test_log)
    test_log.close()


class EventLog():
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def run_event_log(self, driver, test_log):
        gui_lib = Utils(driver)
        self.login_manager.login()

        test_log.start('EventLog')
        test_helper = TestHelper(test_log, driver)

        driver.switch_to_default_content()
        gui_lib.click_element('menu_node_system_tree')
        gui_lib.click_element('menu_node_status')
        gui_lib.click_element('menu_node_event_log')

        driver.switch_to_frame('frame_content')

        table = driver.find_element_by_id('EventBrowserWidget1_table')


        test_log.close()
        self.login_manager.logout()


if __name__ == '__main__':
    main()
