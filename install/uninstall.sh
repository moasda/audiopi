#!/bin/bash
##################################################################################
# Provides: AudioPI (by CSC)
# Description: Steps to unintall AudioPI from RaspberryPI
##################################################################################

#Stop service
sudo systemctl stop audiopi.service

#Remove autostart script
sudo rm /lib/systemd/system/audiopi.service

#Remove logging configuration
sudo rm /etc/logrotate.d/audiopi
sudo rm /etc/rsyslog.d/00_audiopi.conf

#Restart rsyslog
sudo systemctl restart rsyslog

#Remove mocp configuration for USB soundcard
sudo rm ~/.moc/config
sudo rmdir ~/.moc
