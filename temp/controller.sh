#!/bin/bash
##################################################################################
# Provides: AudioPI (by CSC)
# Description: This script controlls all features. Scanned features will
#              be executed in scan-script (e.g. qr_controller.sh).
##################################################################################
AUDIODEV=hw:0

case $1 in
  "scan")
    zbarcam --nodisplay -Sdisable -Sqrcode.enable --prescale=320x240 /dev/video0 | ./qr_controller.sh
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
  "test")
    test="Meine Freundin Conni in den Bergen"
    test=${test//" "/"_"}
    echo $test
    #find /home/pi/music -type d -execdir rename 's/ /_/g' '{}' \+
    ;;
esac
