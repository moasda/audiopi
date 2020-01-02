#Soruce:
#https://github.com/tliero/qudio/blob/master/code/qudio.py

import RPi.GPIO as GPIO
import os
import logging
import time
import subprocess
import select  # for polling zbarcam, see http://stackoverflow.com/a/10759061/3761783

#Configuration
QR_SCANNER_TIMEOUT = 4
MUSIC_BASE_DIRECTORY = "/home/pi/music/"

BOUNCE_TIME = 800

PIN_LED_PHOTO = 23
PIN_BUTTON_SCAN_PLAY = 24
PIN_BUTTON_TOGGLE_PLAY = 17
PIN_BUTTON_VOLUP = 27
PIN_BUTTON_VOLDOWN = 22
PIN_BUTTON_NEXT = 5
PIN_BUTTON_PREVIOUS = 6


#function for button "play/pause"
def play_pause_callback(channel):
    logging.info("PLAY/PAUSE")
    cmd = "mocp -G"
    os.system(cmd)

#function for button "next song"
def next_callback(channel):
    logging.info("NEXT")
    cmd = "mocp -f"
    os.system(cmd)
    ## TODO implement seek

#function for button "previous song"
def prev_callback(channel):
    logging.info("PREV")
    cmd = "mocp -r"
    os.system(cmd)
    ## TODO implement jump to beginning for first x seconds (or if first track)
    ## TODO implement seek

#function for button "volume up"
def volup_callback(channel):
    logging.info("VOLUP")
    cmd = "mocp -v +5"
    os.system(cmd)

#function for button "volume down"
def voldown_callback(channel):
    logging.info("VOLDOWN")
    cmd = "mocp -v -5"
    os.system(cmd)

#function for playing sounds
def play_fail():
    cmd = "mocp -l /home/pi/audiopi/sounds/fail.mp3"
    os.system(cmd)

#function for playing sounds
def play(music_path):
    #Clear current playlsit
    cmd = "mocp -c"
    os.system(cmd)
    #Create new playlist
    cmd = "mocp -a " + music_path
    os.system(cmd)
    #Start playing
    cmd = "mocp -p"
    os.system(cmd)
    logging.info("Play: " + music_path)

#function to scan and play
def scan_and_play_callback(channel):
    #turn LED on for photo
    GPIO.output(PIN_LED_PHOTO, GPIO.HIGH)

    play_status = False

    #scan QR code
    zbarcam = subprocess.Popen(['zbarcam', '--quiet', '--nodisplay', '--raw', '-Sdisable', '-Sqrcode.enable', '--prescale=320x240', '/dev/video0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    poll_obj = select.poll()
    poll_obj.register(zbarcam.stdout, select.POLLIN)
    
    #wait for scan result or timeout
    start_time = time.time()
    poll_result = False
    while ((time.time() - start_time) < QR_SCANNER_TIMEOUT and (not poll_result)):
        poll_result = poll_obj.poll(500)

        if (poll_result):
            qr_code = zbarcam.stdout.readline().rstrip()
            qr_code = qr_code.decode("utf-8") # python3
            logging.info("QR Code: " + qr_code)
            logging.info("QR Code (cp273): " + qr_code.encode(encoding="cp273"))

            if qr_code.startswith("cmd://"):
                play(qr_code)
                play_status = True
            elif qr_code != "":
                #replace blanks with underscore
                qr_code = qr_code.replace(" ", "_")
                #create full path
                full_path = MUSIC_BASE_DIRECTORY + qr_code
                logging.info("full_music_path: " + full_path)
                #play
                play(full_path)
                play_status = True
        else:
            logging.warning('Timeout on zbarcam')

    zbarcam.terminate()
    #turn LED off for photo
    GPIO.output(PIN_LED_PHOTO, GPIO.LOW)

    if play_status == False:
        play_fail()

#function to shutdown the pi
def shutdown_callback(channel):
    logging.info('Shutdown the pi by the right way :)')
    subprocess.call(['sudo', 'shutdown', '-h', 'now'], shell=False)

#Main function
def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s')
    logging.info('Initializing')

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_LED_PHOTO, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(PIN_BUTTON_TOGGLE_PLAY, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #initial value down
    GPIO.setup(PIN_BUTTON_VOLUP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #initial value down
    GPIO.setup(PIN_BUTTON_VOLDOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #initial value down
    GPIO.setup(PIN_BUTTON_NEXT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #initial value down
    GPIO.setup(PIN_BUTTON_PREVIOUS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #initial value down
    GPIO.setup(PIN_BUTTON_SCAN_PLAY, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #initial value down

    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.wait_for_edge(3, GPIO.FALLING)
    GPIO.add_event_detect(3, GPIO.FALLING, callback=shutdown_callback, bouncetime=BOUNCE_TIME)

    logging.info("Register events for buttons")
    GPIO.add_event_detect(PIN_BUTTON_TOGGLE_PLAY, GPIO.FALLING, callback=play_pause_callback, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(PIN_BUTTON_VOLUP, GPIO.FALLING, callback=volup_callback, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(PIN_BUTTON_VOLDOWN, GPIO.FALLING, callback=voldown_callback, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(PIN_BUTTON_NEXT, GPIO.FALLING, callback=next_callback, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(PIN_BUTTON_PREVIOUS, GPIO.FALLING, callback=prev_callback, bouncetime=BOUNCE_TIME)
    BOUNCE_TIME_SCAN = (QR_SCANNER_TIMEOUT * 1000) + BOUNCE_TIME
    GPIO.add_event_detect(PIN_BUTTON_SCAN_PLAY, GPIO.RISING, callback=scan_and_play_callback, bouncetime=BOUNCE_TIME_SCAN)

    logging.info("Start mocp server")
    cmd = "mocp -S"
    os.system(cmd)

    #Play "bootup sound" to show that the pi is ready to use
    cmd = "mocp -l /home/pi/audiopi/sounds/boot_1.wav"
    os.system(cmd)

    try:
        while True:
            logging.info('Waiting for activity')
            time.sleep(10)

    #Exit when Ctrl-C is pressed
    except KeyboardInterrupt:
        logging.info('Shutdown')
        
    finally:
        logging.info('Reset GPIO configuration and close')
        GPIO.cleanup()

#Driver Code 
if __name__ == '__main__': 
    main() 
