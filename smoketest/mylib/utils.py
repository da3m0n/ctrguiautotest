import sys, os, time, shutil
import datetime
from enum import Enum
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium import webdriver
import urllib2
from BeautifulSoup import BeautifulSoup
# from bs4 import BeautifulSoup
# import BeautifulSoup

from smoketest.telnet.Telnet import TelnetClient
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Comment
import requests

import threading

from xml.etree import ElementTree
from xml.dom import minidom


class GlobalFuncs(object):

    def __init__(self):
        pass

    @staticmethod
    def path():
        global path_to_dir
        return path_to_dir

    @staticmethod
    def set_path(p):
        global path_to_dir
        path_to_dir = p

    @staticmethod
    def ensure_path_exists(path):
        import errno
        try:
            print("path to create", path)
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise


#
#
# sub_path = requests.get('http://localhost:3000/next').content
path_to_dir = ''

# GlobalFuncs.ensure_path_exists(path_to_dir)


# def main():
#     utils = Utils
#     utils.print_tree(Utils.log_dir())


class Dates(Enum):
    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12


class Utils(object):
    def __init__(self, driver, test_log):
        self.test_log = test_log
        rt = None
        self.driver = driver
        self.pwd = os.getcwd()
        self.local_time = time.localtime()
        self.date = time.strftime('%d_%B_%Y', self.local_time)
        self.ipAddress = sys.argv[1]

    # @staticmethod
    # def ensure_path_exists(path):
    #     import errno
    #     try:
    #         print("path to create", path)
    #         os.makedirs(path)
    #     except OSError as exception:
    #         if exception.errno != errno.EEXIST:
    #             raise
    #
    # def make_dir(self):
    #     self.get_current_date = 'http://localhost:3000/next'
    #     self.req = requests.get(self.get_current_date)
    #     self.date_run_info = self.req.content
    #     self.path = os.path.join(os.getcwd(), 'logs', *self.date_run_info.split('/'))
    #     self.ensure_path_exists(self.path)

    @staticmethod
    def create_driver(driverName):
        if driverName == "chrome":
            return webdriver.Chrome("C:\ChromeDriver\chromedriver.exe")
        elif driverName == "firefox":
            return webdriver.Firefox()
        elif driverName == "edge":
            return webdriver.Edge()
        elif driverName == "ie":
            return webdriver.Ie()
        else:
            raise Exception("Unknown driver " + driverName)

    def startBrowser(self, driver):
        self.getAddress(driver)
        self.windowInit(driver)

    def loginToRadio(self, driver, loggedIn):
        if loggedIn:
            usr = "root"
            pw = "admin123"
            local_time = time.localtime()
            iso = time.strftime('%Y-%m-%d %H:%M:%S ', local_time)
            print("=====", iso, "=====")

            self.getAddress(driver)
            self.windowInit(driver)

            self.login(driver, usr, pw)
        else:
            print('Already logged in')

    @classmethod
    def login(self, driver, username, password):
        try:
            # find the login element and type in the username
            inputElement = driver.find_element_by_id("username")
            inputElement.send_keys(username)
            # find the password element and type in the password
            inputElement = driver.find_element_by_id("password")
            inputElement.send_keys(password)
            # submit the form
            inputElement.submit()
        except:
            from smoketest.TestLog import TestLog
            from smoketest.TestHelper import TestHelper
            print('login failed')
            dir = Utils.log_dir()
            test_log = TestLog(dir)
            test_helper = TestHelper(test_log, driver, 'smoketest')
            test_helper.assert_true(True,
                                    'Page not loaded OK',
                                    'Page not loaded OK')

            print("Login page not as expected. Exiting...")
            driver.close()
        try:
            # we have to wait for the page to refresh, the last thing that seems to be updated is the title
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "layout_device_name")))
            print('Login Successful')
            time.sleep(5)
        except:
            print("Login unsuccessful")

    # logout, as too many sessions are not allowed
    def logout(self, driver):
        # find the logout button
        try:
            time.sleep(1)
            self.click_element("top_menu_users")
            # logoutTag = driver.find_element_link_text('Logout')

            time.sleep(3)
            logoutTag = self.driver.find_element_by_link_text('Logout')
            logoutTag.click()

            # self.click_element(logoutTag)
            # self.click_element("top_menu_logout")
        except Exception as e:
            print("Logout unsuccessful. This may cause errors with max number of sessions", e)
        else:
            print("Successfully logged out")
        finally:
            time.sleep(2)
            driver.quit()

    # initialise the window size so that all elements are visible
    @classmethod
    def windowInit(self, driver):
        driver.set_window_size(1200, 800)
        # handle = driver.window_handles

    # get the page from the address argument, eg. 192.168.11.11
    @classmethod
    def getAddress(self, driver):
        if len(sys.argv) < 2:
            print("Address argument missing")
            sys.exit()
        address = "http://" + sys.argv[1]
        try:
            response = urllib2.urlopen(address)
            response.close()
        except:
            address = "https://" + sys.argv[1]
        # get page
        driver.get(address)

    # Get the help window
    def getHelp(self, driver):
        help = driver.find_element(By.ID, 'top_menu_help')
        help.click()

        time.sleep(2)
        # check that two windows exist
        handle = driver.window_handles
        if len(handle) != 2:
            print("Incorrect number of windows found")
            print(handle)
            sys.exit()
        time.sleep(5)
        try:
            driver.switch_to_window(handle[1])
            print("changing to help window")
        except:
            print("Unable to change to the help window")
            sys.exit()
        driver.switch_to_frame("body")
        popup = driver.find_element(By.XPATH, "//body/h1").text
        print("Popup:", popup)
        popup = popup.upper()
        return popup

    def click_element(self, element):
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID, element)))
        self.driver.find_element(By.ID, element).click()

    @staticmethod
    def log_dir():
        return os.path.dirname(os.path.dirname(__file__))

    def find_element(self, element):
        try:
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, element)))
            return self.driver.find_element(By.ID, element)
        except NoSuchElementException:
            return 'not found'

    RETRIES = 3
    TIMEOUT_SECONDS = 30

    def find_element_by_id(self, element_id):

        tries = 0
        element = None

        while tries < self.RETRIES:
            try:
                # element = WebDriverWait(self.driver, self.TIMEOUT_SECONDS).until(
                #     lambda l: self.driver.find_element_by_id(element_id))
                element = WebDriverWait(self.driver, self.TIMEOUT_SECONDS).until(
                    EC.visibility_of_element_located((By.ID, element_id)))
            except TimeoutException:
                tries += 1
                # self.switch_to_window(self.window_handles[0])
                continue
            else:
                return element
                # raise NoSuchElementException('Element with id=%s was not found.' % element_id)
                # return

    # @classmethod
    # def get_latest_sw_pack_version(cls):
    #     BUILD_LOCATION = 'http://10.16.0.150:8080/job/CSR1000Release/lastSuccessfulBuild/artifact/BUILD.CSR1000V3/'
    #     try:
    #         soup = BeautifulSoup(urllib2.urlopen(BUILD_LOCATION).read())
    #
    #         cont = soup.find('table', {'class': 'fileList'})
    #         tr = cont.contents
    #         latest = tr[1].contents[1].text
    #         # print('latest: ', latest)
    #         return latest.lstrip('ctr8540-').rstrip('.swpack')
    #     except IOError, msg:
    #         print "Couldn't open URL %s: %s" % (BUILD_LOCATION, str(msg))

    @classmethod
    def get_latest_sw_pack_version(cls, stripped=True):
        BUILD_LOCATION = 'http://10.16.0.150:8080/job/CSR1000Release/lastSuccessfulBuild/artifact/BUILD.CSR1000V3/'

        try:
            soup = BeautifulSoup(urllib2.urlopen(BUILD_LOCATION).read())

            for row in soup('table', {'class': 'fileList'}):
                tds = row('td')[3].contents[0].string
                # print tds.lstrip('ctr8540-').rstrip('.swpack')
                if stripped:
                    return tds.lstrip('ctr8540-').rstrip('.swpack')
                else:
                    return BUILD_LOCATION + tds


        except IOError as msg:
            print("Couldn't open URL %s: %s" % (BUILD_LOCATION, str(msg)))

    @classmethod
    def get_active_sw_version(cls):
        telnet = TelnetClient('root', 'admin123', '10.16.15.113')
        sw_details = telnet.send('show swload', 'Active version:')
        telnet.close()

        for item in sw_details:
            if item.startswith('Active'):
                active_version = item.strip('Active Version:')
                return active_version.lstrip('\'').rstrip('\'')

    @classmethod
    def upload_latest(cls, func):
        telnet = TelnetClient('root', 'admin123', '10.16.15.113', debug=False)
        telnet.send('c t')
        telnet.send('swload')
        command = 'load-uri ' + cls.get_latest_sw_pack_version(False)
        telnet.send(command.encode('ascii', 'ignore'))

        if cls.must_send_abort(telnet):
            print('sending abort command...')
            telnet.send('abort')

        telnet.send('load activate')

        # cls.check_status(telnet)

        rt = RepeatedTimer(15, cls.check_status, telnet, func)

        telnet.close()
        # print(cls.get_latest_sw_pack_version(False))

    @classmethod
    def must_send_abort(cls, telnet):
        progress = telnet.send('show swload')
        for item in progress:
            status = ''
            send_abort = False
            if item.startswith('Current'):
                status = item.strip('Current Status:')

            if status == 'Activate ok (7)':
                send_abort = True
                break
        return send_abort

    @classmethod
    def check_status(cls, timer, telnet, func):
        if telnet is None:
            telnet = TelnetClient('root', 'admin123', '10.16.15.113')

        load_progress = telnet.send('show swload')

        for item in load_progress:
            progress = ''
            status = ''
            if item.startswith('Load'):
                progress = item.strip('Load Progress:')
                print(progress)
            if item.startswith('Current'):
                status = item.strip('Current Status:')
                print(status)
            if item.startswith('Activation'):
                progress = item.strip()

            if status == 'Activate ok (7)':
                if telnet is not None:
                    telnet.close()
                timer.stop()
                print('SOFTWARE LOAD FINISHED...')
                func()

    @classmethod
    def print_tree1(cls, results_dir, test_type):

        # Utils.delete_existing_dir()

        root = ET.Element("resultsFiles")
        # doc = ET.SubElement(root, 'logs')
        root.append(Comment('Auto Generated by print_tree() in mylib/utils.py'))

        dir_contents = os.walk(results_dir + '/logs/').next()
        print('dir_contents', dir_contents)
        for logs_dir in dir_contents[1]:
            field1 = ET.SubElement(root, "testDate")
            field1.set("date", logs_dir.replace('_', ' '))
            field1.set('sortDate', cls.reformat_date(logs_dir))

            # for logs in logs_dir
            # print('results_dir: ' + results_dir + ' logs_dir: ' + logs_dir + ' test_type: ' + test_type)
            next_in_logs = os.walk(results_dir + '/logs/' + logs_dir + '/' + test_type).next()
            print('next_on_logs', next_in_logs)
            # next_in_logs = os.walk(results_dir + '/logs/' + logs_dir).next()
            for xmlfile in next_in_logs[2]:
                field2 = ET.SubElement(field1, "fileName")
                field2.set("file", xmlfile.replace('_', ' '))
                field2.set('fileurl', '/logs/' + logs_dir + '/' + test_type + '/' + xmlfile)

                result = cls.extract_error_count(logs_dir + '/' + test_type + '/' + xmlfile)

                if len(next_in_logs[1]) > 0:
                    in_date_files = os.walk(next_in_logs[0] + '/screenshots').next()
                    print('in_dat_files', in_date_files)
                    el = ET.SubElement(field1, 'screenshots')
                    for image_name in in_date_files[2]:
                        field3 = ET.SubElement(el, "screenshot")
                        field3.set("error", image_name)
                        field3.set('imageurl', '/logs/' + logs_dir + '/' + test_type + '/screenshots/' + image_name)

                total_errors = ET.SubElement(field1, 'errors')
                total_errors.set('totalErrors', result)

        tree = ET.ElementTree(root)
        test_run_type = test_type + 'Dates.xml'
        tree.write(os.path.join(os.path.relpath(Utils.log_dir()), 'logs\\' + test_run_type))  # testDates.xml'))
        # tree.write(os.path.join(os.path.relpath(Utils.log_dir()), 'logs\\testDates.xml'))

    @classmethod
    def extract_error_count1(cls, xmlfile):
        url = 'http://localhost/logs/' + xmlfile
        soup = BeautifulSoup(urllib2.urlopen(url).read())

        error_count = soup.findAll(lambda x: x.name == 'errorcount')
        contents = error_count[0]
        for content in contents.attrs:
            result = content[1]
            break
        return result

    @staticmethod
    def get_dirs(file_path):
        logs_in_dir = []
        for log_file in os.listdir(file_path):
            if os.path.isdir(os.path.join(file_path, log_file)):
                logs_in_dir.append(log_file)

        return logs_in_dir

    @classmethod
    def print_tree(cls, results_dir):
        # Utils.delete_existing_dir()

        root = ET.Element("results")
        # doc = ET.SubElement(root, 'logs')
        root.append(Comment('Auto Generated by print_tree() in mylib/utils.py'))
        # ipAddress = sys.argv[1]

        logs_directory = os.path.join(Utils.log_dir(), 'logs')

        total_errors_count = 0
        path_dir = Utils.get_dirs(results_dir)
        run_number = os.path.basename(results_dir)

        test_run_tag = ET.SubElement(root, 'testRun')
        test_run_tag.set('testRun', run_number)
        test_run_tag.set('outputDir', results_dir)

        for ip_address in Utils.get_dirs(results_dir):
            print 'ip address', ip_address, Utils.get_dirs(results_dir)

            # num_times_run = os.listdir(os.path.join('logs', ip_address))
            # print('run times', num_times_run)
            # print('log_date', log_date, addresses_in_dir, test_dir, os.getcwd())

            ip_addresses_root_tag = ET.Element('ipAddresses')
            output_file = ET.ElementTree(root)

            print 'ss dir', os.listdir((os.path.join(results_dir, ip_address)))

            screenshot_dir = Utils.get_dirs((os.path.join(results_dir, ip_address)))

            if screenshot_dir:
                screen_shots_tag = ET.SubElement(root, 'screenShots')
                screenshot_path = os.path.join(results_dir, ip_address, 'screenshots')

                for ss in os.listdir(screenshot_path):
                    screen_shot_tag = ET.SubElement(screen_shots_tag, 'screenShot')
                    screen_shot_tag.set('imageurl', os.path.join(screenshot_path, ss))
                    # screem_shot_tag.set('screenshotDir', os.path.join())

            else:
                print 'no screenshots', ip_address

            output_file.write(os.path.join(results_dir, ip_address, 'results.xml'))



    @classmethod
    def extract_error_count(cls, xmlfile):

        xmlfile = os.path.join('logs', xmlfile)
        try:
            file = open(xmlfile, 'r')

            tree = ET.parse(file)
            for child in tree.findall('.//errorCount'):
                return int(child.attrib['errorCount'])
        except:
            print('Error opening the file ', xmlfile)

        return 0

    @classmethod
    def reformat_date(cls, date):
        return datetime.datetime.strptime(date, "%d_%B_%Y").strftime("%Y%m%d")

    @staticmethod
    def is_alert_present(driver):
        present_flag = False

        try:
            from selenium.webdriver.common.alert import Alert
            alert = driver.switch_to.alert
            present_flag = True
            alert.accept()

        except NoAlertPresentException:
            pass

        return present_flag

    @classmethod
    def __insert_underscores(cls, str):
        val = str.replace(' ', '_')
        return val

    def open_all(self):
        side_menus = self.driver.find_elements_by_class('side_menu_folder')
        print('side folders', len(side_menus))

    def save_screenshot(self, test_name, test_type):
        test_name = test_name.rstrip('.')

        # screenshots_dir = self.pwd + '\\logs\\' + self.date + '\\' + test_type + '\\screenshots'
        screenshots_dir = os.path.join(GlobalFuncs.path(), self.ipAddress, 'screenshots')

        GlobalFuncs.ensure_path_exists(screenshots_dir)
        self.test_log.store_screenshot_info(test_name, screenshots_dir)
        self.driver.save_screenshot(os.path.join(screenshots_dir, test_name + '.png'))

    @classmethod
    def __make_sure_path_exists(cls, path):
        import errno
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    @staticmethod
    def delete_existing_dir():
        import sys
        ipAddress = sys.argv[1]

        date = time.strftime('%d_%B_%Y', time.localtime())

        screenshots_dir = os.getcwd() + '\\logs\\' + date + '\\smoketest\\' + ipAddress + '\\screenshots'
        if os.path.exists(screenshots_dir):
            shutil.rmtree(screenshots_dir)
        else:
            print(screenshots_dir + ' does not exist.')

    @staticmethod
    def build_id_array(table):
        header_id_arr = []
        headers = table.find_elements_by_tag_name('th')

        for head in headers:
            header_id_arr.append(head.get_attribute('id'))

        return header_id_arr

    @staticmethod
    def build_inner_html_array(id_array):
        ret = []
        for i in id_array:
            val = "document.getElementById(\"" + i + "\").innerHTML=\"\";"
            ret.append(val)
        return ret

    def navigate_to_screen(self, screen_name):
        time.sleep(1)
        breadcrumbs = screen_name.split('/')
        self.__navigate_to_location(breadcrumbs)
        # self.driver.switch_to_frame('frame_content')
        self.test_log.start(breadcrumbs[-1])

    def __navigate_to_location(self, breadcrumbs):
        self.driver.switch_to_default_content()
        self.__navigate_to_location_rec(self.driver, breadcrumbs)

    def __navigate_to_location_rec(self, root, breadcrumbs):
        breadcrumb = breadcrumbs[0]
        if len(breadcrumbs) == 1:
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.LINK_TEXT, breadcrumbs[0])))
            last_el = self.driver.find_element_by_link_text(breadcrumbs[0])
            last_el.click()
        else:
            folder = WebDriverWait(root, 20).until(
                my_visibility_of_elements((By.XPATH, "//div[@class='side_menu_folder']"), breadcrumb))
            expanded = len(folder.find_elements_by_class_name('expanded')) > 0
            if not expanded:
                folder.click()
            self.__navigate_to_location_rec(folder, breadcrumbs[1:])


from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.expected_conditions import _find_elements


class my_visibility_of_elements(object):
    def __init__(self, locator, name):
        self.locator = locator
        self.name = name

    def __call__(self, driver):
        try:
            folders = _find_elements(driver, self.locator)
            for folder in folders:
                # time.sleep(0.25)
                if folder.is_displayed():
                    if folder.text == self.name:
                        return folder

            return False
        except StaleElementReferenceException:
            return False


from threading import Timer


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(self, *self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


# if __name__ == "__main__":
    # main()
