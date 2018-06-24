#!bash
#Checking for root
if [[ "$EUID" -ne 0 ]]; then
  echo "Please run as root"
  #exit 1
fi

echo "============================================="
echo "Bluetooth Unlock Tool For Linux Distributions"
echo "            Setup Version V.7.0              "
echo "============================================="

#5 second countdown timer
secs=$((5))
echo ""
while [[ $secs -gt 0 ]]; do
   echo -ne " Setup will start in: $secs\033[0K\r"
   sleep 1
   : $((secs--))
done

if [ -x "$(which gentoo_release 2>/dev/null)" ];then
release=$(gentoo_release -i)
else
release=$(lsb_release -si)
fi

echo "Distribution: $release"

if [[ -n "$(echo $release | grep -i Ubuntu)" ]]; then
  echo "Using APT"
  sudo apt update
  sudo apt install -y python3 python3-pip bluetooth libbluetooth-dev tar || installfail=1
  sudo -H -u $USER python3 -m pip install pybluez || bluedepfail=1
  echo "Install complete! please run Bluetooth-Unlock.py"
elif [[ -n "$(echo $release | grep -i blackPanther)" ]]; then
    echo "Using blackPanther OS package installer"
    updating repos
    installing python3 python3-pybluez tar libcap-utils
    #other dependencies does not requires
    echo "Recommend for l2ping run as user: setcap 'cap_net_raw,cap_net_admin+eip' /bin/l2ping"

elif [[ -n "$(echo $release | grep -i Fedora )" ]]; then
    echo "Using Yum on Fedora!"
    pkger=`which yum || which dnf`
    $pkger install python3 python3-pip python3-bluez bluez-libs tar || installfail=1
    #other dependencies does not requires
elif [[ -n "$(echo $release | grep -i Gentoo )" ]]; then
  echo "Using yum, WARNING THIS MAY NOT WORK!"
  yum install python3 python3-pip bluetooth libbluetooth-dev tar || installfail=1
  sudo -H -u $USER python3 -m pip install pybluez || bluedepfail=1
else
  echo "Unsupported system please install dependencies yourself, sorry for the inconvenience"
fi

if [[ $installfail == "1" ]]; then
  echo "Install has failed"
elif [[ $bluedepfail == "1" ]]; then
  echo "Pip has failed"
fi
