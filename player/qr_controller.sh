#!/bin/bash
##################################################################################
# Provides: AudioPI (by CSC)
# Description: This read the qr code and executes a command or plays the music.
##################################################################################
AUDIODEV=hw:0

musicpath=/home/pi/music

while true; do
  read qr
  if [[ "$qr" =~ ^QR ]]; then
    echo "Found QR code: $qr" >> log.txt

    #Get qr code "QR-Code:***", we need the string after the ":", for example:
    #music folder: QR-Code:Kokusnuss
    #command:      QR-Code:cmd#sudo reboot
    qrcode=$(echo $qr | cut -d':' -f 2)

    if [[ "$qrcode" =~ ^cmd# ]]; then
      command=$(echo $qrcode | cut -d':' -f 2)
      echo "Execute command: $command" >> log.txt
      exit
    else
      #replace blanks with underscore
      folder=${qrcode//" "/"_"}
      #Create path to the playlist/music files
      playlist=$(echo "$musicpath/$folder")
      echo $playlist >> log.txt
      #Clear current playlsit
      mocp -c
      #Create new playlist
      mocp -a $playlist
      #Start playing
      mocp -p
      exit
    fi
  fi
done
