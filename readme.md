# Requirements

*Content*

1. Shopping list
2. Setup raspian environment (install basic software)
3. Setup audio device for mocp (music over console)
4. Setup AudioPI
5. Start/Stop AudioPi service
6. Information

**todo on Synology: https://gogs.io/**

# 1. Shopping list

|Object|Price|Link|Comment|
|-|-|-|-|
|RASPBERRY PI 2 MODEL B 1 GB RAM|35,49 €|[Conrad](https://www.conrad.de/de/p/raspberry-pi-2-b-1-gb-4-x-0-9-ghz-raspberry-pi-1316978.html)|-|
|RASPBERRY PI CAMERA V2 8MP IR|29,99 €|[Conrad](https://www.conrad.de/de/p/raspberry-pi-camera-module-v2-8mp-cmos-farb-kameramodul-passend-fuer-raspberry-pi-1438999.html)|I think another camera module for ~5-10 € is also enough!|
|Raspberry PI Netztei (original!):|6,90 €|-|-|
|Kabel:|8,99 €|[Amazon](https://www.amazon.de/gp/product/B07KC43D2C/ref=ppx_yo_dt_b_asin_title_o06_s00?ie=UTF8&psc=1)|-|
|Abbiegevorrichtung:|2,98 €|[Amazon](https://www.amazon.de/gp/product/B000YIWM18/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1)|Only needed temporarily. Not needed for product.|
|Kiste:|9,95 €|[Amazon](https://www.amazon.de/gp/product/B016UYWX0E/ref=ppx_yo_dt_b_asin_title_o09_s00?ie=UTF8&psc=1)|-|
|Lötkolben:|15,99 €|[Amazon](https://www.amazon.de/gp/product/B07ZWTCR3G/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)|Only needed temporarily. Not needed for product.|
|Platinen:|6,49 €|[Amazon](https://www.amazon.de/gp/product/B078HV79XX/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1)|-|
|Netzwerk Buchse:|6,99 €|[Amazon](https://www.amazon.de/gp/product/B07TXHRNJD/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1)|-|
|Lautsprecher:|9,99 €|[Amazon](https://www.amazon.de/gp/product/B01HDR5EIK/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1)|-|
|Netzwerkkabel:|3,85 €|[Amazon](https://www.amazon.de/gp/product/B01AWK81VM/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1)|-|
|Raspberry PI Gehäuse:|5,99 €|[Amazon](https://www.amazon.de/gp/product/B00UCSO6SW/ref=ppx_yo_dt_b_asin_title_o09_s00?ie=UTF8&psc=1)|-|
|USB-Soundkarte:|7,99 €|[Amazon](https://www.amazon.de/gp/product/B01N905VOY/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)|-|
|HDMI-Adapter:|7,59 €|[Amazon](https://www.amazon.de/gp/product/B075GZ8DX7/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1)|Only needed temporarily. Not needed for product.|
|SD-Karte (32 GB):|9,00 €|[Amazon](https://www.amazon.de/gp/product/B06XWMQ81P/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1)|-|
|Steckbrett + Zubehör:|12,99 €|[Amazon](https://www.amazon.de/gp/product/B01J79YG8G/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1)|Only needed temporarily. Not needed for product.|
|Knöpfe:|9,99 €|[Amazon](https://www.amazon.de/gp/product/B071WP4ZW4/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1)|-|
|Summe |~200 €|-|-|



# 2. Setup raspian environment

~~~bash
#Systemupdate
sudo apt update
sudo apt upgrade

#QR-Code Software
sudo apt-get install zbar-tools

#Audioplayer for Playlists
sudo apt-get install moc moc-ffmpeg-plugin

#Another Audioplayer for commands
sudo apt install mpg321

#GitClient
sudo apt-get install git

#GitClient configuration
git config --global user.name *"Christian (AudioPI)"*
git config --global user.email *"christian@megaminus.de"*
git config --global core.editor *nano*
~~~

## Configuration respian
~~~bash
#start raspian configuration
sudo raspi-config
#--> activate "camera module"
~~~



# 3. Setup audio device for mocp

## Setup USB audio as default audio device _(for mocp only)_

~~~bash
#Place mocp configuration for USB soundcard
sudo cp ./install/config ~/.moc/config
~~~

## Setup USB audio as default _(for system)_

The USB sound device can be made the default audio device by editing a system file "alsa.conf":

~~~bash
sudo nano /usr/share/alsa/alsa.conf
~~~
Scroll and find the following two lines:

~~~bash
defaults.ctl.card 0
defaults.pcm.card 0
~~~

Change the 0 to a 1 to match the card number of the USB device :

~~~bash
defaults.ctl.card 1
defaults.pcm.card 1
~~~

To save the file and return to the command line use [CTRL-X], [Y], [ENTER].


# 4. Setup AudioPi

~~~bash
#Run install script
chmod 755 ./install/install.sh
./install.sh
~~~



# 5. Start/Stop AudioPi service
~~~bash
#Stop AudioPi service
sudo systemctl stop audiopi.service

#Stop AudioPi service
sudo systemctl start audiopi.service
~~~

**_Attention:_** After AudioPi started, you have 10 Minutes to stop the service until automatical shutdown happens.

# 6. QR-Code Karten erstellen

https://www.the-qrcode-generator.com/

https://www.texttomp3.online/

https://notevibes.com/



# 7. Information

## Other useful commands

~~~bash
#check camera module
raspistill <??????>

#shudown the system
sudo shutdown -h now

#reboot the system
sudo reboot

#Rename folders and replace space with underscore
find ~/music -type d -name '* *' -execdir bash -c 'mv "$1" "${1// /_}"' bash {} \;
~~~

## Useful links

### Tutorials / Examples:

http://www.tilman.de/projekte/musikrakete/

[Template source](https://github.com/tliero/qudio/blob/master/code/qudio.py)

https://github.com/tliero/musikrakete/blob/master/code/piplayer_pulse.py

http://tilman.de/projekte/qudio/

[Raspberry GPIO Pins](https://pinout.xyz/)

[Powerbutton](https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi)

[Power-LED](https://howchoo.com/g/ytzjyzy4m2e/build-a-simple-raspberry-pi-led-power-status-indicator)


### Inspiration:

https://github.com/MiczFlor/RPi-Jukebox-RFID

http://splittscheid.de/selfmade-phoniebox/#3A

