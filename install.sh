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

#Creates temp files and at the end removes them unless terminated
cd ~/ 
mkdir Temporary-BUV1
cd ~/Temporary-BUV1

#Installs python dependencies 
sudo apt update || updatefail=1

sudo apt install -y bluetooth libbluetooth-dev || bluedepfail=1

sudo -H -u $USER python3 -m pip install pybluez || bluedepfail=1

#Gets dependencies from my cloud server
echo "Downloading python3"
wget --https-only -O python.7z https://ecloud.zapto.org/index.php/s/mNFSo8XM4t6JTKe/download && pythonfail=0 || pythonfail=1

#Installs dependencies
sudo apt-get install -y p7zip-full || sudo dpkg --configure -a && sudo apt install -y p7zip-full || p7zipdepfail=1
if [[ $pythonfail == "0" ]]; then
    7z x python.7z

elif [[ $pythonfail == "1" ]]; then
    echo "Can not unzip python.7z due to wget command failing!"
fi  
cd ~/Temporary-BUV1/python 
if [[ $updatefail == "1" ]]; then
    echo "apt update failed!"
fi
if [[ $bluedepfail == "1" ]]; then
    echo "Installing python blueooth dependencies failed!"
fi
if [[ $p7zipdepfail == "1" ]]; then
    echo "Installing p7zip-full failed!"
fi

#Gives user choice to install python3
echo "Do you wish to install python 3 or install yourself? (recommended but will take time!)"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) ./configure --enable-optimizations && make && sudo make install && rm -R ~/Temporary-BUV1 && echo "Installation Complete! please run bluetooth-unlock.py" && exit 0;;
        No ) rm -R ~/Temporary-BUV1 && echo "Installation Complete! please run bluetooth-unlock.py" && exit 0;;
        * ) echo "Invalid Choice"
    esac
done
