import selenium
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, InvalidSelectorException
from selenium.webdriver.support.expected_conditions import _element_if_visible, _find_element, _find_elements
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from smoketest.TestHelper import TestHelper
from smoketest.mylib.utils import Utils


class SmokeTest():
    def __init__(self, driver, test_log):
        self.test_log = test_log
        self.driver = driver
        self.gui_lib = Utils(driver)
        self.test_helper = TestHelper(self.test_log, self.driver)

    def create(self, screen_name, items_to_test, finder):
        breadcrumbs = screen_name.split('/')
        self.__navigate_to_location(breadcrumbs)
        self.driver.switch_to_frame('frame_content')

        self.test_log.start(breadcrumbs[-1])
        # time.sleep(5)
        # self.driver.execute_script("document.getElementById('tableWidget1_3_mapping').innerHTML=\"\";")

        values = []

        for item in items_to_test:
            try:
                label_name = WebDriverWait(self.driver, 30).until(finder.find_label(item))

                vals = finder.find_values(label_name)
                values.append(vals)
            except TimeoutException:
                self.test_helper.assert_true(True,
                                             'Expected ' + item + ' but TimeoutException occurred.',
                                             'Ensure ' + item + ' to be visible')
                break

        for idx, row in enumerate(values):
            name = items_to_test[idx]
            self.test_helper.assert_true(len(name) == 0, 'Expected ' + name + ' to be > 0 but was ' + str(
                len(name)), 'Ensure ' + name + ' visible')
            for td in row:
                self.test_helper.assert_true(len(td) == 0,
                                             'Expected ' + td + ' to be > 0 but was ' + str(
                                                 len(td)),
                                             'Ensure ' + name + ' data visible')

                # finder.test_values(values, self.test_helper)

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


class table_row_header_finder(object):
    def __init__(self):
        self.vals = dict()

    def find_label(self, label):
        return element_locater('th', label)

    def find_values(self, label):
        return find_values_same_row_as_label(label)

        # def test_values(self, values, test_helper):
        #     for row in values:
        #         test_helper.assert_true(len(row[0]) == 0,
        #                                 'Expected ' + row[0] + ' to be > 0 but was ' + str(
        #                                     len(row[0])),
        #                                 'Ensure ' + row[0] + ' header visible')
        #         for cell in row:
        #             test_helper.assert_true(len(cell) == 0,
        #                                     'Expected ' + cell + ' to be > 0 but was ' + str(
        #                                         len(cell)),
        #                                     'Ensure ' + row[0] + ' values visible')


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


class table_column_header_finder(object):
    def __init__(self):
        self.vals = dict()

    def find_label(self, label):
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

    def test_values(self, values, test_helper):
        for item in values:
            # self.assert_value(item[0]['header'])
            test_helper.assert_true(len(item[0]['header']) == 0,
                                    'Expected ' + item[0]['header'] + ' to be > 0 but was ' + str(
                                        len(item[0]['header'])),
                                    'Ensure ' + item[0]['header'] + ' label visible')
            for idx, value in enumerate(item[0]['value']):
                test_helper.assert_true(len(value) == 0,
                                        'Expected ' + value + ' to be > 0 but was ' + str(
                                            len(value)),
                                        'Ensure ' + value + ' values visible')


def find_header_label_index(label):
    headers = label.find_elements_by_xpath('../th|../td')
    for index, item in enumerate(headers):
        if label.text == item.text:
            return index
        index += 1


class td_label_finder(object):
    def __init__(self, label):
        pass

    def find_label(self, label):
        return element_locater('td', self.label)

    def find_values(self, label):
        return find_values_same_row_as_label(label)


def normalize_label(x):
    return " ".join(x.split())


def compare_label(x, y):
    return normalize_label(x) == normalize_label(y)


def find_element(driver, el_type, label):
    words = label.split()
    exps = []
    for word in words:
        exps.append("contains(normalize-space(),%s)" % toXPathStringLiteral(word))

    elements = driver.find_elements_by_xpath("//" + el_type + "[" + " and ".join(exps) + "]")

    norm_label = normalize_label(label)
    for el in elements:
        if el.is_displayed() and normalize_label(el.text) == norm_label:
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


