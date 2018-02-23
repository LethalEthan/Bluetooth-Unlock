#!/usr/bin/python
# imports python modules
import sys
import os
import shutil
from optparse import OptionParser
import subprocess
import time

#Detects python version
if (sys.version_info > (3, 0)):
    print("Python 3 has been detected you may continue")
else:
     sys.exit("Python 2 has been detected please run in python3!")


ENV = "GNOME"  # Can be 'KDE' or 'GNOME'
DEVICEADDR = input("Enter Bluetooth Adress of the device e.g AA:BB:CC:DD:EE:FF: ")#Asks for bluetooth device address

CHECKINTERVAL = 15  # device pinged at this interval (seconds) when screen is unlocked
CHECKREPEAT = 3  # device must be unreachable this many times to lock
mode = 'unlocked'

if __name__ == "__main__":
    while True:
        tries = 0
        while tries < CHECKREPEAT:
            process = subprocess.Popen(['sudo', '/usr/bin/l2ping', DEVICEADDR, '-t', '1', '-c', '1'], shell=False, stdout=subprocess.PIPE)
            process.wait()
            if process.returncode == 0:
                print("ping OK")
                break
            print("ping response code: %d" % (process.returncode))
            time.sleep(1)
            tries = tries + 1

        if process.returncode == 0 and mode == 'locked':
            mode = 'unlocked'
            if ENV == "KDE":
                subprocess.Popen(['loginctl', 'unlock-session 1'], shell=False, stdout=subprocess.PIPE)
            elif ENV == "GNOME":
                subprocess.Popen(['gnome-screensaver-command', '--deactivate'], shell=False, stdout=subprocess.PIPE)

        if process.returncode == 1 and mode == 'unlocked':
            mode = 'locked'
            if ENV == "KDE":
                subprocess.Popen(['loginctl', 'lock-session 1'], shell=False, stdout=subprocess.PIPE)
            elif ENV == "GNOME":
                subprocess.Popen(['gnome-screensaver-command', '--lock'], shell=False, stdout=subprocess.PIPE)
            
        if mode == 'locked':
            time.sleep(1)
        else:
            time.sleep(CHECKINTERVAL)
