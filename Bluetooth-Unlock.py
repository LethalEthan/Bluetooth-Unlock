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
    print("Python 3 has been detected you may continue\n")
else:
    sys.exit("Python 2 has been detected please run in Python3!")


ENV = input("""Please Enter your Desktop Environment can be:
'LOGINCTL' (Recommended)
'KDE' (Doesn't work on older version's)
'GNOME'
'XSCREENSAVER'
'MATE'
'CINNAMON'
""")

ENV = ENV.upper()

if ENV == "LOGINCTL":
 print(ENV,"has been selected")
elif ENV == "KDE":
 print(ENV,"has been selected")
elif ENV == "GNOME":
 print(ENV,"has been selected")
elif ENV == "XSCREENSAVER":
 print(ENV,"has been selected")
else:
 sys.exit("Unidentified Environment exiting")

#DEBUG = input("Would you like to activate debug mode? [Y/N]")#Debug mode prints output of what's going on
#DEBUG = DEBUG.lower()
#if DEBUG == "y":
#	print("DEBUG is active")
#elif DEBUG == "n":
#	print("DEBUG is not active")
#else:
#	sys.exit("Unknown option")
	
DEVICEADDR = input("Enter Bluetooth Adress of the device (e.g AA:BB:CC:DD:EE:FF): ")#Asks for bluetooth device address

CHECKINTERVAL = 3 # device pinged at this interval (seconds) when screen is unlocked
CHECKREPEAT = 2  # device must be unreachable this many times to lock
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
            if ENV == "LOGINCTL":
                subprocess.Popen(['loginctl', 'unlock-session'], shell=False, stdout=subprocess.PIPE)
            elif ENV == "KDE":
                subprocess.Popen(['loginctl', 'unlock-session'], shell=False, stdout=subprocess.PIPE)
            elif ENV == "GNOME":
                subprocess.Popen(['gnome-screensaver-command', '--deactivate'], shell=False, stdout=subprocess.PIPE)
            elif ENV == "XSCREENSAVER":
                subprocess.Popen(['pkill', 'xscreensaver'], shell=False, stdout=subprocess.PIPE)
            elif ENV == "MATE":
                subprocess.Popen(['mate-screensaver-command', '-d'], shell=False, stdout=subprocess.PIPE)	
            elif ENV == "CINNAMON":
                subprocess.Popen(['cinnamon-screensaver-command', '-d'], shell=False, stdout=subprocess.PIPE)
		
        if process.returncode == 1 and mode == 'unlocked':
            mode = 'locked'
            if ENV == "LOGINCTL":
                subprocess.Popen(['loginctl', 'lock-session'], shell=False, stdout=subprocess.PIPE) 
            elif ENV == "KDE":
                subprocess.Popen(['loginctl', 'lock-session'], shell=False, stdout=subprocess.PIPE)
            elif ENV == "GNOME":
                subprocess.Popen(['gnome-screensaver-command', '--lock'], shell=False, stdout=subprocess.PIPE)
            elif ENV == "XSCREENSAVER":
                subprocess.Popen(['xscreensaver-command', '-lock'], shell=False, stdout=subprocess.PIPE)
            elif ENV == "MATE":
                subprocess.Popen(['mate-screensaver-command', '-l'], shell=False, stdout=subprocess.PIPE)
            elif ENV == "CINNAMON":
                subprocess.Popen(['cinnamon-screensaver-command', '-l'], shell=False, stdout=subprocess.PIPE)
            
        if mode == 'locked':
            time.sleep(1)
        else:
            time.sleep(CHECKINTERVAL)
