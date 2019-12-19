### Requirements

*This is important*

1. Setup raspian environment (install basic software)
2. Setup audio device for mocp (music over console)
3. Setup AudioPI
4. Information


### 1. Setup raspian environment

### Code Block
#Systemupdate
sudo apt update
sudo apt upgrade

#Rename command
sudo apt-get install rename

#QR-Code Software
sudo apt-get install zbar-tools

#Audioplayer
sudo apt-get install moc moc-ffmpeg-plugin

#GitClient
sudo apt-get install git

#Konfigurieren des GitClients
git config --global user.name *"Christian (AudioPI)"*
git config --global user.email *"christian@megaminus.de"*
git config --global core.editor *nano*


### Configuration respian

#Konfigurator starten
sudo raspi-config

Activate "Camera"


### 2. Setup audio device for mocp

### Code Block
#Place mocp configuration for USB soundcard
sudo cp ./install/config ~/.moc/config


### 3. Setup AudioPI

### Code Block
#Run install script
chmod 755 ./install/install.sh
./install.sh



### Other useful commands

### Code Block
sudo shutdown -h now
sudo reboot

### Code Block
#Rename folders and replace space with underscore
find ~/music -type d -name '* *' -execdir bash -c 'mv "$1" "${1// /_}"' bash {} \;

### 4. Information

Anleitungen/Beispiele
https://github.com/MiczFlor/RPi-Jukebox-RFID

http://splittscheid.de/selfmade-phoniebox/#3A

Powerbutton:
https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi
