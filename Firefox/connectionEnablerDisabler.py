import os

__author__ = 'rnaude'

os.system("wmic path win32_networkadapter where index=7 call enable")
# os.system("wmic path win32_networkadapter where index=7 call disable")
