#!bash
#checking for root
if [[ "$EUID" -ne 0 ]]; then
  echo "Please run as root"
  exit 1
fi

echo "============================================="
echo "Bluetooth Unlock Tool For Linux Distributions"
echo "            Setup Version V.5.2              "
echo "============================================="

#10 second countdown timer
secs=$((5))
echo "Setup will start in:"
while [[ $secs -gt 0 ]]; do
   echo -ne "$secs\033[0K\r"
   sleep 1
   : $((secs--))
done
release=$(lsb_release -i) || echo "lsb_release not found"
release2=$(gentoo_release -i) || echo "gentoo_release not found"
echo $release
if [[ $release == "Distributor ID:	Ubuntu" ]]; then
  echo "Using apt"
  sudo apt update
  sudo apt install -y python3 python3-pip bluetooth libbluetooth-dev || aptinstallfail=1
  sudo -H -u $USER python3 -m pip install pybluez || bluedepfail=1
  if [[ $aptinstallfail == "1" ]]; then
    echo "Apt has failed"
  elif [[ $bluedepfail == "1" ]]; then
    echo "Pip has failed"
  fi
  echo "Install complete! please run Bluetooth-Unlock.py"
elif [[ $release == "Distributor ID:	Fedora" ]]; then
  echo "Using yum, WARNING THIS MAY NOT WORK!"
  yum install -y python3 python3-pip bluetooth libbluetooth-dev || aptinstallfail=1
  sudo -H -u $USER python3 -m pip install pybluez || bluedepfail=1
elif [[ $release2 == "Distributor ID:	Gentoo" ]]; then
  echo "Using yum, WARNING THIS MAY NOT WORK!"
  yum install -y python3 python3-pip bluetooth libbluetooth-dev || aptinstallfail=1
  sudo -H -u $USER python3 -m pip install pybluez || bluedepfail=1
else
  echo "Unsupported system please install dependencies yourself, sorry for the inconvenience"
fi
