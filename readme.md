### Requirements

*This is important*

1. Setup raspian environment (install basic software)
2. Setup AudioPI (call ./install/install.sh)


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


### Other useful commands

### Code Block
sudo shutdown -h now
sudo reboot
sudo mount 192.168.178.250:/volumes2/daten /mnt/syno_daten
