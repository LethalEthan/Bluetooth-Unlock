#!bash
#checking for root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit 1
fi

echo "============================================="
echo "Bluetooth Unlock Tool For Linux Distributions"
echo "              Setup Version V.1              "
echo "============================================="

secs=$((5 * 2))
echo "Setup will start in:"
while [ $secs -gt 0 ]; do
   echo -ne "$secs\033[0K\r"
   sleep 1
   : $((secs--))
done

#Creates temp files and at the end removes them unless terminated
cd ~/ || echo "error changing directory"
mkdir Temporary
cd ~/Temporary || echo "error changing directory" && exit 1

#Gets dependencies
wget --quiet --https-only -O python.7z https://ecloud.zapto.org/index.php/s/e443rdQyzNxJmTK/download?path=%2F&files=python.7z
sudo apt-get install gnome-screensaver

#Installs dependencies
sudo apt-get install p7zip-full
7z x python.7z
cd python || echo "error changing directory" && exit 1
./configure --enable-optimizations
make
sudo make install
echo "Installation Complete! please run bluetooth-unlock.py" && exit 0
