#!/bin/bash
##################################################################################
# Provides: AudioPI (by CSC)
# Description: Steps to intall AudioPI on RaspberryPI
##################################################################################

#Place autostart script for running at RasbperryPI startup
sudo cp ./audiopi.sh /etc/init.d/audiopi.sh

#Assign the required rights (Read & Write)
sudo chmod 755 /etc/init.d/audiopi.sh

#So that the script is also accessed when booting, we do the following:
sudo update-rc.d audiopi.sh defaults
