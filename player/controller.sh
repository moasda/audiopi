#!/bin/bash
##################################################################################
# Provides: AudioPI (by CSC)
# Required-Start: $syslog
# Required-Stop: $syslog
# Description: This script controlls all features. Scanned features will
#              be executed in scan-script (e.g. qr_controller.sh).
##################################################################################
AUDIODEV=hw:0

case $1 in
  "scan")
    zbarcam --nodisplay -Sdisable -Sqrcode.enable --prescale=320x240 /dev/video0 | /home/pi/audiopi/player/qr_controller.sh
    ;;
  "next")
    echo "Next Song"
    mscp -f
    ;;
 "prev")
    echo "Previous Song"
    mscp -r
    ;;
  "volup")
    echo "volume 5 up"
    mocp -v +5
    ;;
  "voldown")
    echo "volume 5 down"
    mocp -v -5
    ;;
  "play")
    echo "toggle play/pause"
    mocp -G
    #status=$(xmms2 current)
    #if [[ "$status" =~ ^Paused ]]; then
    #  play -q /home/pi/no.wav
    #fi
    ;;
esac
