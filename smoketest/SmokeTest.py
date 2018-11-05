import selenium
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, InvalidSelectorException
from selenium.webdriver.support.expected_conditions import _element_if_visible, _find_element, _find_elements
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from smoketest.TestHelper import TestHelper
from smoketest.mylib.utils import Utils


class SmokeTest:
    def __init__(self, driver, test_log, test_helper):
        self.test_log = test_log
        self.driver = driver
        self.gui_lib = Utils(driver, test_log)
        # self.test_helper = TestHelper(self.test_log, self.driver)
        self.test_helper = test_helper

    # def __navigate_to_screen(self, screen_name):
    #     breadcrumbs = screen_name.split('/')
    #     self.__navigate_to_location(breadcrumbs)
    #     self.driver.switch_to_frame('frame_content')
    #     self.test_log.start(breadcrumbs[-1])

    def create_equipment_test(self, screen_name):
        self.gui_lib.navigate_to_screen(screen_name)

        # self.driver.switch_to_frame("frame_content")
        time.sleep(5)  # added this as I got tired of trying to figure out why it wasn't waiting correctly below
        WebDriverWait(self.driver, 50).until(
            EC.visibility_of_element_located((By.ID, 'ChassisViewWidget1_container')))

        elem = self.driver.find_element_by_xpath("//canvas")

        chassis = self.driver.find_element_by_id('ChassisViewWidget1_container')

        # driver.execute_script("document.getElementById('ChassisViewWidget1_container').innerHTML=\"\";")
        # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, chassis)))

        self.test_helper.assert_true(len(chassis.text) == 0, 'Expected chassis to be displayed but was not',
                                     'Ensure Chassis displayed')

    def create_button_test(self, screen_name, buttons, finder):
        self.gui_lib.navigate_to_screen(screen_name)

        # time.sleep(5)
        # self.driver.execute_script(
        #     "document.getElementsByClassName('alarms_resetChangeIndicators')[0].style.display=\"none\";")
        # self.driver.execute_script(
        #     "document.getElementsByClassName('alarms_resetChangeIndicators')[0].innerHTML=\"\";")

        for button in buttons:
            try:
                button_el = WebDriverWait(self.driver, 30).until(finder.find_buttons(button))
                button_text = button_el.text
                self.test_helper.assert_true(len(button_text) == 0,
                                             'Expected ' + button_text + ' to be > 0, but was ' + str(
                                                 len(button_text)),
                                             'Ensure ' + button_text + ' is displayed.')
            except TimeoutException:
                self.test_helper.assert_true(True,
                                             'Expected ' + button + ' but TimeoutException occurred.',
                                             'Ensure ' + button + ' is displayed.')
                break

    def create2(self, screen_name, items_to_test, finder, just_headers=False):
        self.gui_lib.navigate_to_screen(screen_name)

        # time.sleep(5)
        # self.driver.execute_script("document.getElementById('tableWidget1_3_mapping').innerHTML=\"\";")

        values = []

        for item in items_to_test:
            try:
                label_name = WebDriverWait(self.driver, 30).until(finder.find_label(item))

                if not just_headers:
                    vals = finder.find_values(label_name)
                    values.append(vals)
                else:
                    label = label_name.find_element_by_class_name('syslog_heading')
                    self.test_helper.assert_true(len(label.text) == 0,
                                                 'Expected ' + label.text + ' to be > 0, but was ' + str(
                                                     len(label.text)),
                                                 'Ensure ' + label.text + ' is displayed.')
            except TimeoutException:
                self.test_helper.assert_true(True,
                                             'Expected ' + item + ' but TimeoutException occurred.',
                                             'Ensure ' + item + ' is displayed.')
                break

        for idx, row in enumerate(values):
            name = items_to_test[idx]
            self.test_helper.assert_true(len(name) == 0, 'Expected ' + name + ' to be > 0 but was ' + str(
                len(name)), 'Ensure ' + name + ' visible.')
            for td in row:
                self.test_helper.assert_true(len(td) == 0,
                                             'Expected ' + td + ' to be > 0 but was ' + str(
                                                 len(td)),
                                             'Ensure ' + name + ' data visible.')

    def fix_screen_name(self, name):
        name.split('/')

    def create(self, screen_name):

        try:
            self.gui_lib.navigate_to_screen(screen_name)
            self.gui_lib.is_alert_present(self.driver)

            time.sleep(3)
            # self.driver.execute_script("document.getElementById('tableWidget1_3_mapping').innerHTML=\"\";")

            # WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.ID, "page_loader_container")))
            WebDriverWait(self.driver, 45).until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading_tag")))

            warning_elements = self.driver.find_elements_by_class_name('warning')

            # attr = warning_elements.get_attribute('class')
            # print('warning_elements classname', screen_name, attr, warning_elements[0].text)

            # if attr == 'warning':
            #     display_prop = warning_elements.value_of_css_property('display')
            #     print('display_prop', screen_name, display_prop)

            for el in warning_elements:
                display_prop = el.value_of_css_property('display')

                page_name = screen_name.split('/').pop().replace(' ', '_')

                if display_prop == u'block':
                    self.test_helper.assert_true(True,
                                                 page_name + ' page not loaded OK',
                                                 page_name)
                else:
                    self.test_helper.assert_true(False,
                                                 'Ensure page is displayed.',
                                                 page_name + ' page loaded OK')

        except StaleElementReferenceException as e:
            print('StaleElementException', e)

        return True


def toXPathStringLiteral(s):
    if "'" not in s: return "'%s'" % s
    if '"' not in s: return '"%s"' % s
    return "concat('%s')" % s.replace("'", "',\"'\",'")


def remove_unnecessary_rows(rows):
    new_rows = []
    for idx, row in enumerate(rows):
        header_id = row.get_attribute('id').lower()
        if str(header_id).find('indicator') != -1 or str(header_id).find('header') != -1 or header_id == '':
            rows.remove(row)
            continue
        new_rows.append(row)
    return new_rows


class ButtonFinder(object):
    def __init__(self):
        pass

    @staticmethod
    def find_label(label):
        return element_locater('button', label)

    @staticmethod
    def find_buttons(button):
        print(button)
        return element_locater('button', button)


class TableRowHeaderFinder(object):
    def __init__(self):
        self.vals = dict()

    @staticmethod
    def find_label(label):
        return element_locater('th', label)

    @staticmethod
    def find_values(label):
        return find_values_same_row_as_label(label)


def find_values_same_row_as_label(label):
    row_data = []
    elements = label.find_elements_by_xpath('../td|../th')
    found = False
    for el in elements:
        if el.is_displayed:
            if found and el.text != "":
                row_data.append(el.text)
            elif not found:
                found = el == label
    return row_data


class TableColumnHeaderFinder(object):
    def __init__(self):
        self.vals = dict()

    @staticmethod
    def find_label(label):
        return element_locater('th', label)

    def find_values(self, label):
        rows = label.find_elements_by_xpath('../../tr')
        headers = []
        header_label_index = find_header_label_index(label)
        values_arr = []

        for row_num, row in enumerate(rows):

            header_id = row.get_attribute('id').lower()
            if str(header_id).find('indicator') != -1 or str(header_id).find('header') != -1:
                continue

            cols = row.find_elements_by_xpath('./td')

            vals = cols[header_label_index].text
            self.vals.update({'value': vals})
            values_arr.append(vals)

        return values_arr

    @staticmethod
    def find_headers(label):
        # rows = label.find_elements_by_xpath('//th/div/div')
        # headers = label.find_elements_by_xpath('../th|../td')
        header = label.find_element_by_class_name('syslog_heading')
        headers_arr = []

        if label.text == header.text:
            headers_arr.append(header.text)
        return headers_arr


def find_header_label_index(label):
    headers = label.find_elements_by_xpath('../th|../td')
    for index, item in enumerate(headers):
        if label.text == item.text:
            return index
        index += 1


class TdLabelFinder(object):
    @staticmethod
    def find_label(label):
        return element_locater('td', label)

    @staticmethod
    def find_values(label):
        return find_values_same_row_as_label(label)


class DivTextFinder(object):
    @staticmethod
    def find_label(label):
        return element_locater('div', label)

    @staticmethod
    def find_values(label):
        return find_values_same_row_as_label(label)


class SpanTextFinder(object):
    @staticmethod
    def find_label(label):
        return element_locater('span', label)

    @staticmethod
    def find_values(label):
        return find_values_same_row_as_label(label)


def normalize_label(x):
    return " ".join(x.split())


def compare_label(x, y):
    return normalize_label(x) == normalize_label(y)


def find_base(el):
    children = el.find_elements_by_xpath("./div")
    res = [el]

    for child in children:
        for childEl in find_base(child):
            res.append(childEl)
    return res


def find_element(driver, el_type, label):
    words = label.split()
    exps = []

    for word in words:
        exps.append("contains(normalize-space(),%s)" % toXPathStringLiteral(word))

    elements = driver.find_elements_by_xpath("//" + el_type + "[" + " and ".join(exps) + "]")

    norm_label = normalize_label(label)
    for el in elements:
        if el.is_displayed():
            for el1 in find_base(el):
                if el1.is_displayed() and normalize_label(el1.text) == norm_label:
                    return el
    return False


class element_locater(object):
    def __init__(self, el_type, label):
        self.el_type = el_type
        self.label = label

    def __call__(self, driver):
        return find_element(driver, self.el_type, self.label)


class MisMatchException(Exception):
    def __init__(self, message, errors):
        Exception.__init__(self, message)
        self.errors = errors
