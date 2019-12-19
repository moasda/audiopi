# Pythono3 code to rename multiple files in a directory or folder 
  
import os 
  
# Function to rename multiple files 
def main():
    path = "/home/pi/music/"
    for filename in os.listdir(path): 
        source = path + filename
        destination = path + filename.replace(" ", "_")
        print(source + " --> " + destination)
        os.rename(source, destination) 
  
# Driver Code 
if __name__ == '__main__': 
    # Calling main() function 
    main() 
