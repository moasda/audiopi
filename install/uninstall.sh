#!/bin/bash
##################################################################################
# Provides: AudioPI (by CSC)
# Description: Steps to unintall AudioPI from RaspberryPI
##################################################################################

#Delete mocp configuration for USB soundcard
sudo rm ~/.moc/config

#Take the program out of the Autostart
#sudo update-rc.d -f audiopi.sh remove

#Remove autostart script
#sudo rm /etc/init.d/audiopi.sh

sudo systemctl stop audiopi.service
sudo rm /lib/systemd/system/audiopi.service
