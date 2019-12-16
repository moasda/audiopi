#Soruce:
#https://github.com/tliero/qudio/blob/master/code/qudio.py

import logging
import time
import subprocess
import select  # for polling zbarcam, see http://stackoverflow.com/a/10759061/3761783
from threading import Thread

#Configuration
QR_SCANNER_TIMEOUT = 4


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
def play(uri, service = 'mpd'):
    #socketIO.emit('replaceAndPlay', {'service':service,'uri':uri})


try:
    listener_thread = Thread(target=events_thread)
    listener_thread.daemon = True
    listener_thread.start()

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

            if qr_code.startswith("http://") or qr_code.startswith("https://"):
                play(qr_code, 'webradio')
            elif qr_code.startswith("spotify:"):
                play(qr_code, 'spop')
            else:
                # create full path
                if (qr_code.startswith("/")):
                    qr_code = qr_code[1:]
                full_path = MUSIC_BASE_DIRECTORY + qr_code
                logging.debug("full_path: " + full_path)
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