import time
from smoketest.mylib.utils import Utils
import xml.etree.ElementTree as ET
import os
from xml.etree.ElementTree import Comment


class TestLog(object):
    overall_errors = 0
    num_tests_run = 0
    name = ''
    test_errors = 0
    num_screens = 0

    def __init__(self, name, dir):
        """Class to log errors"""
        self.log = None
        self.doc = None
        self.root = ET.Element(name)
        self.root.append(Comment('Don\'t bother changing. Auto Generated in TestLog.py'))

        self.time = time.localtime()
        self.all_tests_start = time.strftime('%d %B %Y %H:%M:%S', self.time)
        self.url_friendly_start = time.strftime('%d_%B_%Y', self.time)
        self.dir = dir
        el = ET.SubElement(self.root, 'allTestsStart')
        el.set('allTestsStart', self.all_tests_start)

    def start(self, name):
        self.doc = ET.SubElement(self.root, "testScreen", testScreen=name)
        self.num_tests_run += 1
        test_start = time.strftime('%d %B %Y %H:%M:%S ', self.time)

        el = ET.SubElement(self.doc, "testStart")
        el.set("testStart", test_start)

    def log_it(self, data=None):
        el = ET.SubElement(self.doc, 'startTime')
        el.set('blah', data)

    def log_it2(self, count, msg=None, test_name=None):
        self.test_errors += count
        if self.doc == None:
            self.doc = ET.SubElement(self.root, "blahblah", testScreen=test_name)
        el = ET.SubElement(self.doc, 'error')
        el.set('msg', msg)
        el.set('testName', test_name)

    def log_info(self, msg=None):
        el = ET.SubElement(self.doc, 'info')
        el.set('msg', msg)

    def close(self):
        local_time = time.localtime()
        date = time.strftime('%d_%B_%Y', local_time)

        errors = ET.SubElement(self.root, 'errorCount')
        errors.set('errorCount', str(self.test_errors))

        total_tests = ET.SubElement(self.root, 'totalTestCount')
        total_tests.set('totalTestCount', str(self.num_tests_run))
        time.sleep(2) # cause would sometimes return zero screens for whatever reason

        if self.num_screens > 0:
            coverage_percentage = float(self.num_tests_run / float(self.num_screens) * 100)
            coverage = ET.SubElement(self.root, 'coveragePercentage')
            coverage.set('coveragePercentage', ('%.f' % coverage_percentage) + '%')

        tree = ET.ElementTree(self.root)
        log_dir = self.dir + '\\logs\\' + date
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        os.chdir(log_dir)

        path = os.path.abspath(log_dir + '\\' + date + '.xml')
        tree.write(path)

    def add_num_screens(self, num_screens):
        self.num_screens = num_screens
        screens = ET.SubElement(self.root, 'totalScreens')
        screens.set('totalScreens', str(num_screens))
