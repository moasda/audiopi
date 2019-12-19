#!/bin/bash
##################################################################################
# Provides: AudioPI (by CSC)
# Description: Steps to unintall AudioPI from RaspberryPI
##################################################################################

#Stop service
sudo systemctl stop audiopi.service

#Remove autostart script
sudo rm /lib/systemd/system/audiopi.service
