import time
from smoketest.mylib.utils import Utils
import xml.etree.ElementTree as ET
import os

class TestLog(object):
    overall_errors = 0
    num_tests_run = 0
    name = ''

    def __init__(self, name, dir):
        """Class to log errors"""
        self.log = None
        self.doc = None
        self.root = ET.Element("smoketests")
        self.per_test_errors = 0
        self.time = time.localtime()
        self.all_tests_start = time.strftime('%Y-%m-%d %H:%M:%S ', self.time)
        self.dir = dir
        el = ET.SubElement(self.root, 'allTestsStart')
        el.set('allTestsStart', self.all_tests_start)

    def start(self, name):
        # root = ET.Element("root")
        self.doc = ET.SubElement(self.root, "testScreen", testScreen=name)

        test_start = time.strftime('%Y-%m-%d %H:%M:%S ', self.time)
        # ET.SubElement(self.root, 'startTime', str(iso))

        el = ET.SubElement(self.doc, "testStart")
        el.set("teststart", test_start)

        # field2 = ET.SubElement(doc, "field2")
        # field2.set("name", "asdfasd")
        # field2.text = "some vlaue2"

        self.num_tests_run += 1

    def log_it(self, data=None):
        el = ET.SubElement(self.doc, 'startTime')
        el.set('blah', data)

    def log_it2(self, count, msg=None, test_name=None):
        el = ET.SubElement(self.doc, 'error')
        el.set('msg', msg)
        el.set('testName', test_name)

    def close(self):
        local_time = time.localtime()
        date = time.strftime('%d-%m-%Y', local_time)

        tree = ET.ElementTree(self.root)
        log_dir = self.dir + '\\logs\\' + date
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        os.chdir(log_dir)

        path = os.path.abspath(log_dir + '\\' + date + '.xml')
        tree.write(path)
