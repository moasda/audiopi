#Soruce:
#https://github.com/tliero/qudio/blob/master/code/qudio.py

import logging
import time
import subprocess
import select  # for polling zbarcam, see http://stackoverflow.com/a/10759061/3761783
from threading import Thread

#Configuration
QR_SCANNER_TIMEOUT = 4
MUSIC_BASE_DIRECTORY = "/home/pi/music/"

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s')
logging.info('Initializing')

#function for button "play/pause"
def play_callback(channel):
    logging.info("PLAY/PAUSE")
    #socketIO.emit('pause')

#function for button "next song"
def next_callback(channel):
    logging.info("NEXT")
    #socketIO.emit('next')
    ## TODO implement seek

#function for button "previous song"
def prev_callback(channel):
    logging.info("PREV")
    #socketIO.emit('prev')
    ## TODO implement jump to beginning for first x seconds (or if first track)
    ## TODO implement seek

#function for button "volume up"
def prev_callback(channel):
    logging.info("VOLUP")

#function for button "volume down"
def prev_callback(channel):
    logging.info("VOLDOWN")

#function for playing sounds
def play(music_path):
    #mocp -c
    #mocp -a $playlist
    #mocp -p
    #Clear current playlsit
    subprocess.Popen(['mocp', '-c'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #Create new playlist
    subprocess.Popen(['mocp', '-a '+ music_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #Start playing
    subprocess.Popen(['mocp', '-p'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


try:
    #listener_thread = Thread(target=events_thread)
    #listener_thread.daemon = True
    #listener_thread.start()

    while True:
        #scan QR code
        zbarcam = subprocess.Popen(['zbarcam', '--quiet', '--nodisplay', '--raw', '-Sdisable', '-Sqrcode.enable', '--prescale=320x240', '/dev/video0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        poll_obj = select.poll()
        poll_obj.register(zbarcam.stdout, select.POLLIN)
        
        #wait for scan result (or timeout)
        start_time = time.time()
        poll_result = False
        while ((time.time() - start_time) < QR_SCANNER_TIMEOUT and (not poll_result)):
            poll_result = poll_obj.poll(100)

        if (poll_result):
            qr_code = zbarcam.stdout.readline().rstrip()
            qr_code = qr_code.decode("utf-8") # python3
            logging.info("QR Code: " + qr_code)
            print("QR Code: " + qr_code)

            if qr_code.startswith("cmd://"):
                play(qr_code)
            else:
                #replace blanks with underscore
                qr_code.replace(" ", "_")
                #create full path
                full_path = MUSIC_BASE_DIRECTORY + qr_code
                logging.debug("full_music_path: " + full_path)
                play(full_path)
            
        else:
            logging.warning('Timeout on zbarcam')
            play(SOUND_SCAN_FAIL)

        zbarcam.terminate()

# Exit when Ctrl-C is pressed
except KeyboardInterrupt:
    logging.info('Shutdown')
    print("Shutdown")
    
finally:
    logging.info('Reset GPIO configuration and close')
    print("Reset GPIO configuration and close")
#    GPIO.cleanup()            