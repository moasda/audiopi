#!/bin/bash
AUDIODEV=hw:0
musicpath=/home/pi/music

while true; do
  read qr
  if [[ "$qr" =~ ^QR ]]; then
    echo "Found QR code: $qr" >> test.txt
    folder=$(echo $qr | cut -d':' -f 2)
    playlist=$(echo "$musicpath/$folder")
    echo $playlist >> test.txt
    mocp -c
    mocp -a $playlist
    mocp -p
    exit
  fi
  #echo "QR-Code not found: $qr" >> test.txt
  #sleep 1
done
