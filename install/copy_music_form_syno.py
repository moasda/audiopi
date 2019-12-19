
import os

#Function to mount sync directory
def mount():
    #crate mount point
    cmd = "sudo mkdir /mnt/syno_music"
    os.system(cmd)
    cmd = "sudo chmod 755 /mnt/syno_music"
    os.system(cmd)
    #mount folder from synology to mout point (read only)
    cmd = "sudo mount -r 192.168.178.29:/volume2/music /mnt/syno_music"
    os.system(cmd)

#Function to unmount sync directory
def unmount():
    #unmount synology folder
    cmd = "sudo umont /mnt/syno_music"
    os.system(cmd)
    #remove mount point
    cmd = "sudo rmdir /mnt/syno_music"
    os.system(cmd)

#Function to sync directory
def sync():
    src_path = "/mnt/syno_music"
    dst_path = "/home/pi/music/"
    for filename in os.listdir(src_path): 
        #todo
        destination = dst_path + filename.replace(" ", "_")
        print(source + " --> " + destination)
        #os.rename(source, destination) 
        #rsync -rtv source_folder/ destination_folder/

#Main function to sync music directory with synology
def main():
    mount()
    sync()
    unmount()

# Driver Code 
if __name__ == '__main__': 
    # Calling main() function 
    main() 
