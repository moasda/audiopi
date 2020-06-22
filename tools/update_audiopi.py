#!/usr/bin/python3
import configparser
import os
import subprocess

#load config
config = configparser.ConfigParser()
config.read_file(open('/home/pi/audiopi.cfg'))
SOUND_START = config['tools.update']['AudioStart']
SOUND_STOP = config['tools.update']['AudioStop']

#Main function to sync music directory with synology
def main():
    os.system("sudo systemctl stop audiopi.service") #stop service, because of shutdown timer
    subprocess.call(['mpg321', SOUND_START], shell=False)
    os.system("cd ~/audiopi; git pull")
    subprocess.call(['mpg321', SOUND_STOP], shell=False)
    os.system("sudo systemctl start audiopi.service")

# Driver Code 
if __name__ == '__main__': 
    # Calling main() function 
    main() 
