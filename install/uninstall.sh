#!/bin/bash
##################################################################################
# Provides: AudioPI (by CSC)
# Description: Steps to unintall AudioPI from RaspberryPI
##################################################################################

#Take the program out of the Autostart
sudo update-rc.d -f audiopi.sh remove

#Remove autostart script
sudo rm /etc/init.d/audiopi.sh
