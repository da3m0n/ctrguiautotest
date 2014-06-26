import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smoketest.systemconfiguration.dateTime import DateTime
from smoketest.TestLog import TestLog
from smoketest.systemconfiguration.manufactureDetails import ManufactureDetails
from smoketest.mylib.LoginHandler import LoginHandler
from smoketest.mylib.utils import Utils
from smoketest.systemconfiguration.powerOverEthernet import PowerOverEthernet
from smoketest.systemconfiguration.sysAbout import SystemAbout
from smoketest.systemconfiguration.sysInfo import SystemInformation
from smoketest.systemconfiguration.equipmentView import EquipmentView
from optparse import OptionParser


def main():
    parser = OptionParser(usage="usage: %prog ipAddress browser")
    # parser.add_option("-c", "--chelp", help="Add arguments for IP Address for radio and target browser")
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("wrong number of arguments")

    run_all = RunAll()
    run_all.run_all()

    Utils.print_tree(Utils.log_dir())


from enum import Enum


class ComparisonResult(Enum):
    LATEST = 1
    ACTIVE = 2
    SAME = 3


def reformat_for_compare(swpack):
    # if build is master substitute master for 99.99.99 for easier comparison
    if swpack.find('master') != -1:
        return swpack.replace('master', '99.99.99')
    else:
        return swpack


def must_download_latest(active_swpack, latest_swpack):
    active = active_swpack.split('.')
    decoded_latest = latest_swpack.encode('ascii', 'ignore')
    latest = decoded_latest.split('.')

    for i in range(0, min(len(active), len(latest))):
        if compare(int(active[i]), int(latest[i])) == ComparisonResult.SAME or compare(int(active[i]), int(
                latest[i])) == ComparisonResult.ACTIVE:
            res = False
        else:
            res = True
    return res


def compare(active, latest):
    if active < latest:
        return ComparisonResult.LATEST
    elif active > latest:
        return ComparisonResult.ACTIVE
    else:
        return ComparisonResult.SAME


def determine_latest_swpack(active_swpack, latest_swpack):
    active = active_swpack.split('.')
    decoded_latest = latest_swpack.encode('ascii', 'ignore')
    latest = decoded_latest.split('.')

    for i in range(0, min(len(active), len(latest))):
        if compare(int(active[i]), int(latest[i])) == 'same':
            continue
        elif compare(int(active[i]), int(latest[i])) == 'active':
            return 'active'
        else:
            return 'latest'
    return len(active) > len(latest)


class RunAll():
    def __init__(self):
        self.dir = Utils.log_dir()
        self.test_log = TestLog('All Tests', self.dir)
        print('init')

    def run_all(self):
        active_sw_version = Utils.get_active_sw_version()
        latest_swpack = Utils.get_latest_sw_pack_version()

        # dummies for tests
        active_sw_version = 'master.12.1919'
        latest_swpack = 'master.12.1919'

        # swpack = determine_latest_swpack(reformat_for_compare(active_sw_version), reformat_for_compare(latest_swpack))
        get_latest = must_download_latest(reformat_for_compare(active_sw_version), reformat_for_compare(latest_swpack))

        if get_latest:
            print ('Get latest sw pack...')
            Utils.upload_latest(self.do_rest)
        else:
            print ('Using latest, don\'t need to upload latest... ')
            self.do_rest()

    def do_rest(self):
        print('Gonna run the smoketests...')
        driver = Utils.create_driver(sys.argv[2])

        Utils.delete_existing_logfile(self.dir)

        login_handler = LoginHandler()
        login_handler.start(driver)

        test_log = TestLog('All Tests', self.dir)
        # test_log.start('Equipment View')

        equipment_view = EquipmentView(login_handler)
        equipment_view.run_equipment_view(driver, test_log)

        sys_info = SystemInformation(login_handler)
        sys_info.run_system_information(driver, test_log)

        date_time = DateTime(login_handler)
        date_time.run_date_time(driver, test_log)

        # These need to be updated as they have been moved
        # sys_about = SystemAbout(login_handler)
        # sys_about.run_system_about(driver, test_log)

        # manu_details = ManufactureDetails(login_handler)
        # manu_details.run_manufacture_details(driver, test_log)

        # poe = PowerOverEthernet(login_handler)
        # poe.run_poe(driver, test_log)

        login_handler.end(driver)


if __name__ == "__main__":
    main()