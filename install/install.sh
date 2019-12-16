#!/bin/bash
##################################################################################
# Provides: AudioPI (by CSC)
# Description: Steps to intall AudioPI on RaspberryPI
##################################################################################

#Place autostart script for running at RasbperryPI startup
#sudo cp ./audiopi_autostart.sh /etc/init.d/audiopi.sh
sudo cp ./audiopi.service /lib/systemd/system/audiopi.service

#Assign the required rights (read & write & execute)
#sudo chmod 755 /etc/init.d/audiopi.sh
#sudo chmod 755 /lib/systemd/system/audiopi.service

#So that the script is also accessed when booting, we do the following:
#sudo update-rc.d audiopi.sh defaults

#run service
sudo systemctl daemon-reload
sudo systemctl start audiopi.service

#autostart service while booting
sudo systemctl enable audiopi.service
