#!/bin/bash
AUDIODEV=hw:0
while true; do
  read qr
  read qr2
  if [[ "$qr" =~ ^QR ]]; then
    echo "------------------------------"
    echo $qr
    echo "------------------------------"
    artist=$(echo $qr | cut -d':' -f 3)
    echo "artist: $artist"
    album=$(echo $qr2 | cut -d':' -f 2-)
    echo "album: $album"
    if [[ "$album" =~ ^http ]]; then
      killall zbarcam
      #xmms2 stop
      #xmms2 clear
      #xmms2 add $album
      #play -q /home/pi/source/rbar/ok.wav
      #xmms2 play
      exit
      s=""
      echo "play1"
    else
      #s=$(xmms2 search album:"$album" | egrep -e "$album")
      echo "play2"
    fi
    if [[ -n "$s" ]]; then
      killall zbarcam
      #xmms2 stop
      #xmms2 clear
      #xmms2 add album:"$album" -o "tracknr"
      #play -q /home/pi/source/rbar/ok.wav
      #xmms2 play
      echo "play3"
      exit
    else
      #xmms2 stop
      #play -q /home/pi/source/rbar/no.wav
      echo "no file found"
    fi
    echo "next try in 5 seconds"
    sleep 5
  fi
  echo "QR-Code: $qr"
  sleep 1
done
