import subprocess
import sys
import signal
import sys
import os
import xml.etree.ElementTree as ET

import time
import requests
from xml.etree.ElementTree import Comment

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smoketest.mylib.utils import Utils


def ensure_path_exists(path):
    import errno
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


sub_path = requests.get('http://localhost:3000/next').content
path_to_dir = os.path.join(os.getcwd(), 'logs', *sub_path.split('/'))
ensure_path_exists(path_to_dir)


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    [p.kill() for p in opens]
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

opens = []
root = ET.Element("ipAddresses")
root.append(Comment('Auto Generated in multi-run.py'))


def run_some(start, end):
    for i in range(start, end):
        time.sleep(2)

        opens.append(subprocess.Popen(["c:\\Python27\\python.exe", "./runAll.py", sys.argv[i], "chrome", path_to_dir]))

    [p.wait() for p in opens]


logs_dir = os.path.join(Utils.log_dir(), 'logs')

run_dates_path = os.path.join(Utils.log_dir(), 'logs', "runInfo.txt")

if not os.path.exists(run_dates_path):

    run_dates_file = open(run_dates_path, "a+")

    for date in Utils.get_dirs(logs_dir):
        for run in os.listdir(os.path.join(Utils.log_dir(), 'logs', date)):
            print 'date', date, 'list', os.listdir(os.path.join(Utils.log_dir(), 'logs', date))
            run_dates_file.write(date + '/' + run + '\n')

else:
    run_dates_file = open(run_dates_path, "a+")
    run_dates_file.write(sub_path + '\n')

run_dates_file.close()

for i in range(1, len(sys.argv)):
    field = ET.SubElement(root, "ipAddress").text = sys.argv[i]

tree = ET.ElementTree(root)
tree.write(os.path.join(path_to_dir, 'ip-addresses.xml'))

step = 3
for i in range(1, len(sys.argv), step):
    run_some(i, min(i + step, len(sys.argv)))

# print('path_to_dir', path_to_dir)
# Utils.print_tree(path_to_dir, 'smoketest')
Utils.print_tree(path_to_dir)

# print('****', os.path.join(os.path.relpath(GlobalFuncs2.path())))
