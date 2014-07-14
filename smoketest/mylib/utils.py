import sys, os, time
import datetime
from enum import Enum
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium import webdriver
import urllib2
from BeautifulSoup import BeautifulSoup
# from bs4 import BeautifulSoup
# import BeautifulSoup
from smoketest.telnet.Telnet import TelnetClient
import threading

from xml.etree import ElementTree
from xml.dom import minidom


def main():
    utils = Utils
    utils.print_tree(Utils.log_dir())


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
    def __init__(self, driver):
        rt = None
        self.driver = driver
        # resultFile =

    @staticmethod
    def create_driver(driverName):
        if driverName == "chrome":
            return webdriver.Chrome("C:\ChromeDriver\chromedriver.exe")
        elif driverName == "firefox":
            return webdriver.Firefox()
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
            inputElement = driver.find_element_by_name("Login")
            inputElement.send_keys(username)
            # find the password element and type in the password
            inputElement = driver.find_element_by_name("Password")
            inputElement.send_keys(password)
            # submit the form
            inputElement.submit()
        except:
            print("Login page not as expected. Exiting...")
            driver.quit()
        try:
            # we have to wait for the page to refresh, the last thing that seems to be updated is the title
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "layout_device_name")))
            print('Login Successful')
            time.sleep(5)
        except:
            print("Login unsuccessful")

    #logout, as too many sessions are not allowed
    def logout(self, driver):
        try:
            #find the logout button
            self.click_element("top_menu_users")
            self.click_element("top_menu_logout")
            print("Successfully logged out")
            login_button = Utils.find_element('login')
            if not login_button is None:
                driver.quit()
        except:
            try:
                #otherwise check whether already on the login page
                driver.find_element_by_name("Login")
                driver.quit()
            except:
                print("Logout unsuccessful. This may cause errors with max number of sessions")


    #initialise the window size so that all elements are visible
    @classmethod
    def windowInit(self, driver):
        driver.set_window_size(1200, 800)
        #handle = driver.window_handles

    #get the page from the address argument, eg. 192.168.11.11
    @classmethod
    def getAddress(self, driver):
        if len(sys.argv) < 2:
            print("Address argument missing")
            sys.exit()
        address = "http://" + sys.argv[1]
        #get page
        driver.get(address)

    #Get the help window
    def getHelp(self, driver):
        help = driver.find_element(By.ID, 'top_menu_help')
        help.click()

        time.sleep(2)
        #check that two windows exist
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
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, element)))
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
        raise NoSuchElementException('Element with id=%s was not found.' % element_id)

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
    def print_tree(cls, results_dir):
        import xml.etree.ElementTree as ET
        from xml.etree.ElementTree import Comment

        root = ET.Element("resultsFiles")
        # doc = ET.SubElement(root, 'logs')
        root.append(Comment('Do Not Change. Auto Generated by print_tree() in utils.py'))

        dir_contents = os.walk(results_dir + '/logs/').next()
        for logs_dir in dir_contents[1]:
            field1 = ET.SubElement(root, "testDate")
            field1.set("date", logs_dir.replace('_', ' '))
            field1.set('sortDate', cls.reformat_date(logs_dir))

            # for logs in logs_dir
            next_in_logs = os.walk(results_dir + '/logs/' + logs_dir).next()
            for xmlfile in next_in_logs[2]:
                field2 = ET.SubElement(field1, "fileName")
                field2.set("file", xmlfile.replace('_', ' '))
                field2.set('fileurl', '/logs/' + logs_dir + '/' + xmlfile)

                result = cls.extract_error_count(logs_dir + '/' + xmlfile)

                if len(next_in_logs[1]) > 0:
                    in_date_files = os.walk(next_in_logs[0] + '/screenshots').next()
                    el = ET.SubElement(field1, 'screenshots')

                    for image_name in in_date_files[2]:
                        field3 = ET.SubElement(el, "screenshot")
                        field3.set("error", image_name)
                        field3.set('imageurl', '/logs/' + logs_dir + '/screenshots/' + image_name)

                total_errors = ET.SubElement(field1, 'errors')
                total_errors.set('totalErrors', result)

        tree = ET.ElementTree(root)
        tree.write(os.path.join(os.path.relpath(Utils.log_dir()), 'logs\\testDates.xml'))

    @classmethod
    def extract_error_count(cls, xmlfile):
        url = 'http://localhost/logs/' + xmlfile
        soup = BeautifulSoup(urllib2.urlopen(url).read())

        error_count = soup.findAll(lambda x: x.name == 'errorcount')
        contents = error_count[0]
        for content in contents.attrs:
            result = content[1]
            break
        return result

    @classmethod
    def reformat_date(cls, date):
        return datetime.datetime.strptime(date, "%d_%B_%Y").strftime("%Y%m%d")


    @classmethod
    def insert_underscores(cls, str):
        val = str.replace(' ', '_')
        return val


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


if __name__ == "__main__":
    main()
