#!/usr/bin/env python3
#Imports python modules
import sys
import os
import shutil
import argparse
import subprocess
import time
import getpass
import configparser
try:
    import bluetooth
    from bluetooth import *
    import bluetooth._bluetooth as bt
except:
    print("Cannot import the bluetooth modules!")
    print("Please run install.sh!")
    sys.exit(1)

#Detects python version
if (sys.version_info > (3, 0)):
    print("Python 3 has been detected you may continue\n")
else:
    sys.exit("Python 2 has been detected please run in Python3!")

#Things for imports
parser = argparse.ArgumentParser()
config = configparser.ConfigParser()
from distutils.spawn import find_executable

#Reads configuration file
config.read("config.ini")

#Variables
USER = getpass.getuser() #For the thank you message
GET_DEVADDR = 1 #For setup when no config is found
SELECT_ENV = 1 #For setup when no config is found

#Checks for a new version
if config.has_option("VERSION", "version"):
    VERSION = config.get("VERSION", "version")
else:
    sys.exit("VERSION/CONFIG NOT FOUND!")
UPDATE = input("Would you like to check for an update? [Y/N] ")
UPDATE = UPDATE.upper()
if UPDATE == "Y":
    print("Downloading Update.ini from ecloud...")
    os.system("wget -q -O Update.ini https://ecloud.zapto.org/index.php/s/AKeEkGxC2nww2KX/download")
    print("Done!\n")
    config.read("Update.ini")
    if config.has_option("NOTICES", "notices"):
        NOTICES = config.get("NOTICES", "notices")
    else:
        print("Cannot find any notices, Download may have failed!")
    if config.has_option("NEWVERSION", "newversion"):
        NEWVERSION = config.get("NEWVERSION", "newversion")
    else:
        print("Cannot find new version!")
    print(NOTICES,"\n")
    if config.has_option("NEWVERSION", "newversion"):
        if NEWVERSION > VERSION:
            config.clear()
            print("New version found:", NEWVERSION)
            UPDATE_C = input("Would you like to Download updates? [Y/N] ")
            UPDATE_C = UPDATE_C.upper()
            if UPDATE_C == "Y":
                print("Downloading Update from ecloud...")
                os.system("wget -q -O Update.tar.gz https://ecloud.zapto.org/index.php/s/7CM8NtHjZfDr9KS/download")
                print("Downloaded!, please extract new files in current directory!")
            else:
                print("Not downloading update")
        elif NEWVERSION < VERSION:
            config.clear()
            print("Version installed is higher than the version specified in update config!")
        elif NEWVERSION == VERSION:
            config.clear()
            print("Latest version installed!")
        else:
            config.clear()
            print("If you see this message then config has no version information!")
elif UPDATE == "N":
    print("\nNot checking for updates!")
else:
    print("Unknown response!")
config.read("config.ini")
time.sleep(2)
#Loads the options from the config and loads them into a local variable
#Loads Desktop Environment option
if config.has_option("DESKTOP", "env"):
    print("\nDesktop Environment found, using:")
    SELECT_ENV = 0
    ENV = config.get("DESKTOP", "env")
    print(ENV)
#Loads Device Address
if config.has_option("DEVADDR", "devaddr"):
    print("\nDevice Address found, using:")
    GET_DEVADDR = 0
    DEVADDR = config.get("DEVADDR", "devaddr")
    print(DEVADDR)
time.sleep(3)
#User can see what Desktop Environments are available (not all are detected)
if SELECT_ENV == 1:
    AVAILDE = input("\nWould you like to see the available desktop environments? [Y/N] ")
    AVAILDE = AVAILDE.upper()
    if AVAILDE == "Y":
            gnome_screensaver = {'GNOME': 'gnome-screensaver'}
            for gnome_env in gnome_screensaver:
                if find_executable(gnome_screensaver[gnome_env]):
                    print("GNOME has been found")
                else:
                    print("GNOME has not found")
            mate_screensaver = {'MATE': 'mate-screensaver-command'}
            for mate_env in mate_screensaver:
                if find_executable(mate_screensaver[mate_env]):
                    print("MATE has been found")
                else:
                    print("MATE has not been found")
            x_screensaver = {'XSCREENSAVER': 'xscreensaver'}
            for x_env in x_screensaver:
                if find_executable(x_screensaver[x_env]):
                    print("XSCREENSAVER has been found")
                else:
                    print("XSCREENSAVER has not been found")
            print("")
    elif AVAILDE == "N":
        print("Not displaying the available desktop environments")
    else: ("Uknown response")
#Select Desktop Environment menu
if SELECT_ENV == 1:
    #Detects if these desktop evironments are available
    ENV = input("""Please Enter your Desktop Environment can be:
    "LOGINCTL" (Recommended) (Don't use sudo)
    "KDE" (Doesn"t work on older versions)
    "GNOME"
    "XSCREENSAVER"
    "MATE"
    "CINNAMON"
    """)
    ENV = ENV.upper()
    if ENV == "LOGINCTL":
        print(ENV,"has been selected\n")
    elif ENV == "KDE":
        print(ENV,"has been selected\n")
    elif ENV == "GNOME":
        print(ENV,"has been selected\n")
    elif ENV == "XSCREENSAVER":
        print(ENV,"has been selected\n")
    elif ENV == "MATE":
        print(ENV,"has been selected\n")
    elif ENV == "CINNAMON":
        print(ENV,"has been selected\n")
    else:
        sys.exit("Unidentified Environment exiting")
    config["DESKTOP"] = {"ENV": (ENV)}
    with open("config.ini", "w") as configfile:
        config.write(configfile)

print("\nBluetooth-Unlock is a free open-source project and always will be")
print("I would like you to consider donating to allow me to do other projects")
print("The donation links are on the website: https://lethalethan.github.io/Bluetooth-Unlock/")
print("Thanks :)\n")

#Debug mode prints extra information of what's going on
DEBUG = input("Would you like to activate debug mode? [Y/N] ")
DEBUG = DEBUG.upper()
if DEBUG == "Y":
	print("DEBUG is active")
elif DEBUG == "N":
	print("DEBUG is not active")
else:
	sys.exit("Unknown option")

#Code containing thank you message and device detection
print("")
print("Thank you for using Bluetooth-Unlock",VERSION ,USER ,"\n")
if GET_DEVADDR == 1:
    print("Searching for nearby devices...\n")
    nearby = discover_devices(lookup_names = True)
    print(nearby,"\n")
    DEVADDR = input("Enter Bluetooth Address of the device (e.g AA:BB:CC:DD:EE:FF): ")#Asks for bluetooth device address
    config["DEVADDR"] = {"DEVADDR": (DEVADDR)}
    with open("config.ini", "w") as configfile:
        config.write(configfile)
elif GET_DEVADDR == 0:
    print("Device Address is", DEVADDR)
time.sleep(2)
#Prints information
if DEBUG == "Y":
    print("\nThis is the sections found in config.ini")
    print(config.sections())
    print("Desktop Environment is", ENV)
    print("Device Address is",DEVADDR,"\n")
    time.sleep(4)
else: time.sleep(1)
print("\nThank you to these contributors: jose1711, maaudrana, blackPanther OS")
print("jose1711 has improved the code of this project")
print("maaudrana is making a logo for this project")
print("blackPanther OS has improved/optimized the code of this project")
print("Thanks to all of them :)\n")
time.sleep(4)
#Variables for Main code
CHECKINTERVAL = 3 # device pinged at this interval (seconds) when screen is unlocked min:3
CHECKREPEAT = 2  # device must be unreachable this many times to lock
mode = "unlocked"

#Main code for Bluetooth-Unlock
#Return code 0 is when the command has ran successfully
#Return code 1 is when the command has failed to reach the device
print("Bluetooth-Unlock is now active!")
while True:
    tries = 0
    while tries < CHECKREPEAT:
        #Checks for the device
        time.sleep(CHECKINTERVAL)
        check = subprocess.Popen(["sudo", "l2ping", DEVADDR, "-t", "1", "-c", "1"], shell=False, stdout=subprocess.PIPE)
        check.wait()
        retcode = check.returncode
        if retcode == 0 and DEBUG == "Y":
            print("ping OK!")
            break
        elif retcode > 0 and DEBUG == "Y":
            #Prints returncode when debug is active
            print("ping response code: %d" % (retcode))
            time.sleep(1)
            tries = tries + 1

        if retcode == "Can\'t create socket: Operation not permitted":
            print("Couldn't create a socket due to permissions")

    #Unlocks when the device IS found
    if retcode == 0 and mode == "locked":
        mode = "unlocked"
        if ENV == "LOGINCTL":
            os.system("loginctl unlock-session")
        elif ENV == "KDE":
            os.system("loginctl unlock-session")
        elif ENV == "GNOME":
            os.system("gnome-screensaver-command -d")
        elif ENV == "XSCREENSAVER":
            os.system("pkill xscreensaver")
        elif ENV == "MATE":
            os.system("mate-screensaver-command -d")
        elif ENV == "CINNAMON":
            os.system("cinnamon-screensaver-command -d")

    #Locks when the device ISN'T found
    if retcode > 0 and mode == "unlocked":
        mode = "locked"
        if ENV == "LOGINCTL":
            os.system("loginctl lock-session")
        elif ENV == "KDE":
            os.system("loginctl lock-session")
        elif ENV == "GNOME":
            os.system("gnome-screensaver-command -l")
        elif ENV == "XSCREENSAVER":
            os.system("xscreensaver-command -lock")
        elif ENV == "MATE":
            os.system("mate-screensaver-command -l")
        elif ENV == "CINNAMON":
            os.system("cinnamon-screensaver-command -l")

    if mode == "locked":
        time.sleep(1)
    else:
        time.sleep(CHECKINTERVAL)
