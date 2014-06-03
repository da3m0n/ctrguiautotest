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


def determine_latest_swpack(active_sw_pack, latest_sw_pack):
    print 'packA: %s, packB: %s' % (active_sw_pack, latest_sw_pack)

    active = active_sw_pack.split('.')
    decoded_latest = latest_sw_pack.encode('ascii', 'ignore')
    latest = decoded_latest.split('.')

    for i in range(0, len(active)):
        if compare2(int(active[i]), int(latest[i])) == 'same':
            continue
        elif compare2(int(active[i]), int(latest[i])) == 'active':
            return 'active'
        else:
            return 'latest'


def compare2(active, latest):
    if active < latest:
        return 'latest'
    elif active > latest:
        return 'active'
    else:
        return 'same'


def compare(a, b):
    if a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0


class RunAll():
    def __init__(self):
        self.dir = os.path.dirname(__file__)
        self.test_log = TestLog('All Tests', self.dir)
        print('init')

    def run_all(self):
        active_sw_version = Utils.get_active_sw_version()
        latest_swpack = Utils.get_latest_sw_pack_version()

        # dummies for tests
        # active_sw_version = 'master.12.1915'
        # latest_swpack = 'master.12.1913'

        swpack = determine_latest_swpack(reformat_for_compare(active_sw_version), reformat_for_compare(latest_swpack))
        if swpack == 'latest':
            print ('go get latest pack')
            Utils.upload_latest(self.do_rest)
        else:
            print ('using latest, don\'t need to upload')
            self.do_rest()

    def do_rest(self):
        print('Gonna run the smoketests...')
        self.driver = Utils.create_driver(sys.argv[2])

        print('running all tests')
        Utils.delete_existing_logfile(self.dir)

        login_handler = LoginHandler()
        login_handler.start(self.driver)

        test_log = TestLog('All Tests', self.dir)

        equipment_view = EquipmentView(login_handler)
        equipment_view.run_equipment_view(self.driver, test_log)

        sys_info = SystemInformation(login_handler)
        sys_info.run_system_information(self.driver, test_log)
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