#!bash
#checking for root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
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
cd ~/
mkdir Temporary
cd ~/Temporary
