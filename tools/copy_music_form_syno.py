#!/usr/bin/python3
import configparser
import os
import subprocess

#load config
config = configparser.ConfigParser()
config.read_file(open('/home/pi/audiopi.cfg'))
WIN_USER = config['tools.copy']['WinUser']
WIN_PASS = config['tools.copy']['WinPassword']
PATH_SOURCE = config['tools.copy']['PathSource']
PATH_TARGET = config['tools.copy']['PathTarget']
PATH_MOUNT = config['tools.copy']['PathMount']
SOUND_START = config['tools.copy']['AudioStart']
SOUND_STOP = config['tools.copy']['AudioStop']


#Function to mount sync directory
def mount():
    #crate mount point
    cmd = "sudo mkdir " + PATH_MOUNT
    os.system(cmd)
    cmd = "sudo chmod 755 " + PATH_MOUNT
    os.system(cmd)
    #mount folder from synology to mout point (read only)
    if WIN_USER != "" and WIN_PASS != "":
        cmd = "sudo mount -t cifs"+ PATH_SOURCE +" "+ PATH_MOUNT +" -o username=<user>,password=<password>"
    else:
        cmd = "sudo mount -r " + PATH_SOURCE + " " + PATH_MOUNT
    os.system(cmd)


#Function to unmount sync directory
def unmount():
    #unmount synology folder
    cmd = "sudo umount " + PATH_MOUNT
    os.system(cmd)
    #remove mount point
    cmd = "sudo rmdir " + PATH_MOUNT
    os.system(cmd)


#Function to sync directory
def sync():
    for filename in os.listdir(PATH_MOUNT): 
        #todo
        source_folder =  PATH_MOUNT + filename
        destination_folder = PATH_TARGET + filename.replace(" ", "_")
        print(source_folder + " --> " + destination_folder)
        cmd = "sudo rsync -rvu --delete --exclude '@*' --exclude '#recycle' --exclude '*.ini' '" + source_folder + "/' '" + destination_folder + "/'"
        os.system(cmd)


#Main function to sync music directory with synology
def main():
    os.system("sudo systemctl stop audiopi.service") #stop service, because of shutdown timer
    mount()
    #play sound with 50% loudness (g) and no output (q)
    subprocess.call(['mpg321', '-q', SOUND_START, '-g', '50'], shell=False)
    sync()
    subprocess.call(['mpg321', '-q', SOUND_STOP, '-g', '50'], shell=False)
    unmount()
    os.system("sudo systemctl start audiopi.service")


# Driver Code 
if __name__ == '__main__': 
    # Calling main() function 
    main() 
