# Requirements

*This is important*

1. Setup raspian environment (install basic software)
2. Setup audio device for mocp (music over console)
3. Setup AudioPI
4. Information


# 1. Setup raspian environment

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
~~~
Activate "Camera"


## Set USB Audio as Default Audio Device

The USB sound device can be made the default audio device by editing a system file “alsa.conf” :

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


# 2. Setup audio device for mocp

~~~bash
#Place mocp configuration for USB soundcard
sudo cp ./install/config ~/.moc/config
~~~

# 3. Setup AudioPI

~~~bash
#Run install script
chmod 755 ./install/install.sh
./install.sh
~~~

# 4. Information

## Other useful commands

~~~bash
#shudown the system
sudo shutdown -h now

#reboot the system
sudo reboot

### Code Block
#Rename folders and replace space with underscore
find ~/music -type d -name '* *' -execdir bash -c 'mv "$1" "${1// /_}"' bash {} \;
~~~

## Useful links

Anleitungen/Beispiele:

https://github.com/MiczFlor/RPi-Jukebox-RFID

http://splittscheid.de/selfmade-phoniebox/#3A

Powerbutton:

https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi

Power-LED:

https://howchoo.com/g/ytzjyzy4m2e/build-a-simple-raspberry-pi-led-power-status-indicator
