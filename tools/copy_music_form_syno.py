
import os
import subprocess

#config
PATH_SOURCE = "192.168.178.29:/volume2/music/audiobox_laura"
PATH_TARGET = "/home/pi/music/"
PATH_MOUNT = "/mnt/syno_music/"

#Function to mount sync directory
def mount():
    #crate mount point
    cmd = "sudo mkdir " + PATH_MOUNT
    os.system(cmd)
    cmd = "sudo chmod 755 " + PATH_MOUNT
    os.system(cmd)
    #mount folder from synology to mout point (read only)
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
    mount()
    subprocess.call(['mpg321', '/home/pi/audiopi/sounds/abgleich_daten_startet.mp3'], shell=False)
    sync()
    subprocess.call(['mpg321', '/home/pi/audiopi/sounds/abgleich_daten_fertig.mp3'], shell=False)
    unmount()

# Driver Code 
if __name__ == '__main__': 
    # Calling main() function 
    main() 
