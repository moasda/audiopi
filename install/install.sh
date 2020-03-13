#!/bin/bash
##################################################################################
# Provides: AudioPI (by CSC)
# Description: Steps to intall AudioPI on RaspberryPI
##################################################################################

#Place autostart script for running at RasbperryPI startup
#sudo cp ./audiopi_autostart.sh /etc/init.d/audiopi.sh
sudo cp ./audiopi.service /lib/systemd/system/audiopi.service

#run service
sudo systemctl daemon-reload
sudo systemctl start audiopi.service

#autostart service while booting
sudo systemctl enable audiopi.service

#Place mocp configuration for USB soundcard
sudo mkdir ~/.moc
sudo cp ./config ~/.moc/config
