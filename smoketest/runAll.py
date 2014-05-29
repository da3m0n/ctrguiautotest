import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smoketest.systemconfiguration.dateTime import DateTime
from smoketest.TestLog import TestLog
from smoketest.systemconfiguration.equipmentView2 import EquipmentView
from smoketest.systemconfiguration.manufactureDetails import ManufactureDetails
from smoketest.mylib.LoginHandler import LoginHandler
from smoketest.mylib.utils import Utils
from smoketest.systemconfiguration.powerOverEthernet import PowerOverEthernet
from smoketest.systemconfiguration.sysAbout import SystemAbout
from smoketest.systemconfiguration.sysInfo2 import SystemInformation

from optparse import OptionParser


def main():
    parser = OptionParser(usage="usage: %prog ipAddress browser")
    # parser.add_option("-c", "--chelp", help="Add arguments for IP Address for radio and target browser")
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("wrong number of arguments")

    run_all = RunAll()
    run_all.run_all()


def reformat_for_compare(swpack):
    # if build is master substitute master for 99.99.99
    if swpack.find('master') != -1:
        return swpack.replace('master', '99.99.99')
    else:
        return swpack


def determine_latest_swpack(packA, packB):
    print 'packA: %s, packB: %s' % (packA, packB)

    a = packA.split('.')
    b = packB.encode('ascii', 'ignore')
    b1 = b.split('.')

    for i in range(0, len(a)):
        print 'A: %s, B: %s' % (type(a[i]), type(b1[i]))
        print 'A: %s, B: %s' % (a[i], b1[i])
        print(compare(int(a[i]), int(b1[i])))


def compare(a, b):
    if a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0


class RunAll():
    def __init__(self):
        # self.driver = Utils.create_driver(sys.argv[2])
        # self.testLog = TestLog()
        print('init')

    @staticmethod
    def run_all():
        # active_sw_version = Utils.get_active_sw_version()
        active_sw_version = '2.102.0.12.1912'
        latest_swpack = Utils.get_latest_sw_pack_version()

        # print "Active version: %s Latest Version: %s" % (
        #     reformat_for_compare(active_sw_version), reformat_for_compare(latest_swpack))

        determine_latest_swpack(reformat_for_compare(active_sw_version), reformat_for_compare(latest_swpack))

        # print('running all tests')
        # Utils.delete_existing_logfile(os.path.dirname(__file__))
        #
        # login_handler = LoginHandler()
        # login_handler.start(self.driver)
        #
        # test_log = TestLog('All Tests', os.path.dirname(__file__))
        #
        # equipment_view = EquipmentView(login_handler)
        # equipment_view.run_equipment_view(self.driver, test_log)
        #
        # sys_info = SystemInformation(login_handler)
        # sys_info.run_system_information(self.driver, test_log)
        #
        # date_time = DateTime(login_handler)
        # date_time.run_date_time(self.driver, test_log)
        #
        # sys_about = SystemAbout(login_handler)
        # sys_about.run_system_about(self.driver, test_log)
        #
        # manu_details = ManufactureDetails(login_handler)
        # manu_details.run_manufacture_details(self.driver, test_log)
        #
        # poe = PowerOverEthernet(login_handler)
        # poe.run_poe(self.driver, test_log)
        #
        # login_handler.end(self.driver)


if __name__ == "__main__":
    main()