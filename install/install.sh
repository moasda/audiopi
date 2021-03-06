#!/bin/bash
##################################################################################
# Provides: AudioPI (by CSC)
# Description: Steps to intall AudioPI on RaspberryPI
##################################################################################

#create folder for audio sources
mkdir ~/music

#Place audiopi config to user home (only when file not exists)
if ! test -f ~/audiopi.cfg; then
    cp ~/audiopi/install/audiopi_config.cfg ~/audiopi.cfg
fi

#Place autostart script for running at RasbperryPI startup
sudo cp ~/audiopi/install/audiopi.service /lib/systemd/system/audiopi.service

#Setup Logrotation for /var/log/audiopi.log
sudo cp ~/audiopi/install/audiopi_logrotate /etc/logrotate.d/audiopi
sudo cp ~/audiopi/install/00_audiopi.conf /etc/rsyslog.d/00_audiopi.conf

#create initial log file
sudo touch /var/log/audiopi.log
sudo chown root:adm /var/log/audiopi.log

#Restart rsyslog
sudo systemctl restart rsyslog

#run service
sudo systemctl daemon-reload
sudo systemctl start audiopi.service

#autostart service while booting
sudo systemctl enable audiopi.service

#Place mocp configuration for USB soundcard and headphone
mkdir ~/.moc
if ! test -f ~/.moc/config; then
    #create backup
    cp ~/.moc/config ~/.moc/config_backup
fi
if ! test -f ~/.moc/config_headphone; then
    #create backup
    cp ~/.moc/config_headphone ~/.moc/config_headphone_backup
fi
cp ~/audiopi/install/mocp_config ~/.moc/config
cp ~/audiopi/install/mocp_config_headphone ~/.moc/config_headphone
