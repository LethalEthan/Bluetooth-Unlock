#!/usr/bin/python
# imports python modules
import sys
import os
import shutil
from optparse import OptionParser
import subprocess
import time

ENV = "GNOME"  # Can be 'KDE' or 'GNOME'
DEVICEADDR = "AA:BB:CC:DD:EE:FF" # bluetooth device address
CHECKINTERVAL = 30  # device pinged at this interval (seconds) when screen is unlocked
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
                subprocess.Popen(['loginctl', 'unlock-session', '1'], shell=False, stdout=subprocess.PIPE)
            elif ENV == "GNOME":
                subprocess.Popen(['gnome-screensaver-command', '--deactivate'], shell=False, stdout=subprocess.PIPE)

        if process.returncode == 1 and mode == 'unlocked':
            mode = 'locked'
            if ENV == "KDE":
                subprocess.Popen(['loginctl', 'lock-session', '1'], shell=False, stdout=subprocess.PIPE)
            elif ENV == "GNOME":
                subprocess.Popen(['gnome-screensaver-command', '--lock'], shell=False, stdout=subprocess.PIPE)
            
        if mode == 'locked':
            time.sleep(1)
        else:
            time.sleep(CHECKINTERVAL)
