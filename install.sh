#!bash
#checking for root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit 1
fi

echo "============================================="
echo "Bluetooth Unlock Tool For Linux Distributions"
echo "            Setup Version V.4.2              "
echo "============================================="

#10 second countdown timer
secs=$((5))
echo "Setup will start in:"
while [ $secs -gt 0 ]; do
   echo -ne "$secs\033[0K\r"
   sleep 1
   : $((secs--))
done

#Installs python dependencies 

sudo apt install -y bluetooth libbluetooth-dev || bluedepfail=1

sudo -H -u $USER python3 -m pip install pybluez || bluedepfail=1

if [[ $bluedepfail == "1" ]]; then
    echo "Installing python blueooth dependencies failed!"
fi
