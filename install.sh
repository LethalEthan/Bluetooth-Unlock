#!/bin/bash
#Checking for root
if [[ "$EUID" -ne 0 ]]; then
  echo "Please run as root, so sudo password isn't required later on..."
  #exit 1
fi

echo "============================================="
echo "Bluetooth Unlock Tool For Linux Distributions"
echo "            Setup Version V.8.0              "
echo "============================================="

#5 second countdown timer
secs=$((5))
echo ""
while [[ $secs -gt 0 ]]; do
   echo -ne " Setup will start in: $secs\033[0K\r"
   sleep 1
   : $((secs--))
done

#Preset Variables to 0
installfail=0
bluedepfail=0

#OS Check (Gentoo and Ubuntu/Debian supported)
if [ -x "$(which gentoo_release 2>/dev/null)" ];then
release=$(gentoo_release -i)
else
release=$(lsb_release -si)
fi

echo "Distribution: $release"

#Install for Ubuntu
if [[ -n "$(echo $release | grep -i Ubuntu)" ]]; then
  echo "Using APT on Ubuntu!"
  sudo apt update
  sudo apt install -y python3 python3-pip bluetooth libbluetooth-dev tar || installfail=1
  sudo -H -u $USER python3 -m pip install pybluez || bluedepfail=1
  echo "Install complete! please run Bluetooth-Unlock.py"

elif [[ -n "$(echo $release | grep -i Debian)" ]]; then
  echo "Using APT on Debian!"
  echo "WARNING: This hasn't been tested on a Debian system, it may not work!"
  sudo apt-get update
  sudo apt-get install -y python3 python3-pip bluetooth libbluetooth-dev tar || installfail=1
  sudo -H -u $USER python3 -m pip install pybluez || bluedepfail=1
  echo "Install complete! please run Bluetooth-Unlock.py"

#Install for blackPanther
elif [[ -n "$(echo $release | grep -i blackPanther)" ]]; then
  echo "Using blackPanther OS package installer"
  updating repos
  installing python3 python3-pybluez tar libcap-utils
  #Does not require other dependencies
  echo "Recommend for l2ping run as user: setcap 'cap_net_raw,cap_net_admin+eip' /bin/l2ping"
  echo "Install complete! please run Bluetooth-Unlock.py"

#Install for Fedora
elif [[ -n "$(echo $release | grep -i Fedora )" ]]; then
  echo "Using Yum on Fedora!"
  pkger=`which yum || which dnf`
  $pkger install python3 python3-pip python3-bluez bluez-libs tar || installfail=1
  echo "Install complete! please run Bluetooth-Unlock.py"
  #Does not require other dependencies

#Install for Gentoo
elif [[ -n "$(echo $release | grep -i Gentoo )" ]]; then
  echo "Using Yum on Gentoo!"
  echo "WARNING: This hasn't been tested on a Gentoo system, it may not work!"
  yum install python3 python3-pip bluetooth libbluetooth-dev tar || installfail=1
  sudo -H -u $USER python3 -m pip install pybluez || bluedepfail=1
  echo "Install complete! please run Bluetooth-Unlock.py"

#Message for Unsupported OS's
else
  echo "Unsupported system please install dependencies yourself, sorry for the inconvenience"
  echo "Dependencies: python3 python3-pip bluetooth libbluetooth-dev tar"
  echo "PIP Dependencies: pybluez"
  echo "If you feel this OS should be supported please create a feature request in the issue section"
fi

#Fail Detect
if [[ $installfail == "0" ]]; then
  echo "Install has worked!"
elif [[ $bluedepfail == "0" ]]; then
  echo "Pip has worked!"
  exit 0
fi

if [[ $installfail == "1" ]]; then
  echo "Install has failed"
elif [[ $bluedepfail == "1" ]]; then
  echo "Pip has failed"
  exit 1
fi
