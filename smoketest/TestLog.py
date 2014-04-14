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

    def start(self, name):
        # root = ET.Element("root")
        doc = ET.SubElement(self.root, "testName", testName=name)
        timetup = time.localtime()
        iso = time.strftime('%Y-%m-%d %H:%M:%S ', timetup)
        # ET.SubElement(self.root, 'startTime', str(iso))

        field1 = ET.SubElement(doc, "field1")
        field1.set("name", "blah")
        field1.text = "some value1"

        # field2 = ET.SubElement(doc, "field2")
        # field2.set("name", "asdfasd")
        # field2.text = "some vlaue2"


        self.name = name
        self.log = open('logs/testLog.log', 'a')
        self.log.write('========= Running ' + name + ' Tests\n')
        self.log.write('Started tests at ' + iso + '\n')
        self.num_tests_run += 1

    def log_it(self, data):
        self.log.write('   - ' + data + '\n')
        self.subElement(data)
        # ET.SubElement(self.root, data)

    @classmethod
    def subElement(self, data):
        ET.SubElement()

    def end_log(self, error_count):
        self.per_test_errors = error_count

        if error_count == 0:
            self.log.write('========= Tests Passed. End ' + self.name + '\n')
        else:
            self.log.write('- ' + str(error_count) + ' failures.\n')
            self.log.write('========= End ' + self.name + ' tests.\n')
            self.overall_errors += 1

    def close(self):
        self.log.write('All Tests Finished. ' + str(self.num_tests_run) + ' Screen Tests run. ' + str(
            self.overall_errors) + ' Tests failed.\n')
        self.log.write('\n')
        self.log.close()
        tree = ET.ElementTree(self.root)
        tree.write('logs/testLog.xml')


    def open_tag(self, testName):
        self.log_it('<testName>' + testName)

    def add_tag(self, data):
        self.log_it()

    def close_tag(self):
        self.log_it('</testName>')