import time
from smoketest.mylib.utils import Utils
import xml.etree.ElementTree as ET


class TestLog(object):
    overall_errors = 0
    num_tests_run = 0
    name = ''

    def __init__(self):
        """Class to log errors"""
        # Utils.delete_existing_logfile('testLog.log')
        self.log = None
        print('Creating testLog...')
        self.root = ET.Element("smoketests")
        self.per_test_errors = 0
        self.doc = None

    def start(self, name):
        # root = ET.Element("root")
        self.doc = ET.SubElement(self.root, "testScreen", testScreen=name)
        timetup = time.localtime()
        iso = time.strftime('%Y-%m-%d %H:%M:%S ', timetup)
        # ET.SubElement(self.root, 'startTime', str(iso))

        field1 = ET.SubElement(self.doc, "time")
        field1.set("starttime", iso)

        # field2 = ET.SubElement(doc, "field2")
        # field2.set("name", "asdfasd")
        # field2.text = "some vlaue2"

        self.num_tests_run += 1

    def log_it(self, data=None):
        el = ET.SubElement(self.doc, 'startTime')
        el.set('blah', data)

    def log_it2(self, count, msg=None, testName=None):
        el = ET.SubElement(self.doc, 'error')
        el.set('msg', msg)
        el.set('testName', testName)

    def close(self):
        tree = ET.ElementTree(self.root)
        tree.write('logs/testLog.xml')
