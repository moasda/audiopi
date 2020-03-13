#!/usr/bin/python3

import RPi.GPIO as GPIO
import logging
from logging.handlers import RotatingFileHandler
import time
import subprocess
import select  #for polling zbarcam, see http://stackoverflow.com/a/10759061/3761783
import threading 
import mocp #own script


#Configuration
QR_SCANNER_TIMEOUT = 4
MUSIC_BASE_DIRECTORY = "/home/pi/music/"
SYSTEM_SOUND_DIRECTORY = "/home/pi/audiopi/sounds/"
LOG_FILE = "/tmp/audiopi.log"

BOUNCE_TIME = 800

PIN_LED_PHOTO = 23
PIN_BUTTON_SCAN_PLAY = 18
PIN_BUTTON_TOGGLE_PLAY = 17
PIN_BUTTON_VOLUP = 25
PIN_BUTTON_VOLDOWN = 24
PIN_BUTTON_NEXT = 22
PIN_BUTTON_PREVIOUS = 27
PIN_BUTTON_SHUTDOWN = 3


#function for button "play/pause"
def play_pause_callback(channel):
    mocp.toggle_play_pause()


#function for button "next song"
def next_callback(channel):
    mocp.next_song()


#function for button "previous song"
def prev_callback(channel):
    mocp.previous_song()


#function for button "volume up"
def volup_callback(channel):
    mocp.volume_up()


#function for button "volume down"
def voldown_callback(channel):
    mocp.volume_down()


#function for playing sounds
def play_fail():
    title = SYSTEM_SOUND_DIRECTORY + 'fail.mp3'
    mocp.play_system_sound(title)


#function for playing sounds
def play(music_path):
    mocp.play_folder(music_path)


#function for playing sounds from an URL
def play_stream(url):
    mocp.play_url(url)


#function to scan and play
def scan_and_play_callback(channel):
    #turn LED on for photo
    GPIO.output(PIN_LED_PHOTO, GPIO.HIGH)

    #stop playing
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
            #qr_code = qr_code.replace("羹", "ü")
            logging.info("QR Code: " + qr_code)
            
            if qr_code.startswith("cmd://"):
                command = qr_code[6:]
                play_status = True
            elif qr_code.startswith("stream://"):
                play_stream(qr_code[9:])
                play_status = True
            elif qr_code.startswith("timer://"):
                seconds = qr_code[8:]
                timer = threading.Timer(int(seconds), play_fail) 
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


#function to shutdown button
def shutdown_callback(channel):
    mocp.stop()
    time.sleep(0.5)
    title = SYSTEM_SOUND_DIRECTORY + 'shutdown.mp3'
    mocp.play_system_sound(title)
    time.sleep(0.5)
    system_shutdown()


#function to shutdown the pi
def system_shutdown():
    logging.info('Shutdown the pi by the right way :)')
    subprocess.call(['sudo', 'shutdown', '-h', 'now'], shell=False)


#Main function
def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s')
    log_handler = RotatingFileHandler(LOG_FILE, maxBytes=5000000, backupCount=5) #5 MB
    logging.addHandler(log_handler)
    logging.info('Initializing')

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_LED_PHOTO, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(PIN_BUTTON_SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_BUTTON_TOGGLE_PLAY, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_BUTTON_VOLUP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_BUTTON_VOLDOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_BUTTON_NEXT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_BUTTON_PREVIOUS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_BUTTON_SCAN_PLAY, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    logging.info("Register events for buttons")
    GPIO.add_event_detect(PIN_BUTTON_SHUTDOWN, GPIO.FALLING, callback=shutdown_callback, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(PIN_BUTTON_TOGGLE_PLAY, GPIO.FALLING, callback=play_pause_callback, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(PIN_BUTTON_VOLUP, GPIO.FALLING, callback=volup_callback, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(PIN_BUTTON_VOLDOWN, GPIO.FALLING, callback=voldown_callback, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(PIN_BUTTON_NEXT, GPIO.FALLING, callback=next_callback, bouncetime=BOUNCE_TIME+500)
    GPIO.add_event_detect(PIN_BUTTON_PREVIOUS, GPIO.FALLING, callback=prev_callback, bouncetime=BOUNCE_TIME+500)
    BOUNCE_TIME_SCAN = ((QR_SCANNER_TIMEOUT * 1000) + BOUNCE_TIME + 2000) #Timeouts addieren und in ms umrechnen
    GPIO.add_event_detect(PIN_BUTTON_SCAN_PLAY, GPIO.RISING, callback=scan_and_play_callback, bouncetime=BOUNCE_TIME_SCAN)

    #Start mocp server
    mocp.start_server()

    #Play "bootup sound" to show that the pi is ready to use
    title = SYSTEM_SOUND_DIRECTORY + 'boot.mp3'
    mocp.play_system_sound(title)

    shutdown_timer_running = False

    try:
        while True:
            logging.info('Waiting for activity')
            time.sleep(10)

            if (mocp.check_mocp_playing() == False) and (shutdown_timer_running == False):
                shutdown_timer = threading.Timer(900.0, system_shutdown) #shutdown in 15 minutes
                shutdown_timer.start()
                logging.info('Shutdowntimer started!')
                shutdown_timer_running = True
            elif (mocp.check_mocp_playing() == True) and (shutdown_timer_running == True):
                shutdown_timer.cancel()
                logging.info('Shutdowntimer canceled!')
                shutdown_timer_running = False

    #Exit when Ctrl-C is pressed
    except KeyboardInterrupt:
        logging.info('Shutdown')
        
    finally:
        logging.info('Reset GPIO configuration and close process! AudioPi says goodbye...')
        GPIO.cleanup()

#Driver Code 
if __name__ == '__main__': 
    main() 
