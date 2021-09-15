#!/usr/bin/python3

import RPi.GPIO as GPIO
import configparser
import logging
from logging.handlers import RotatingFileHandler
import time
import subprocess
import select  #for polling zbarcam, see http://stackoverflow.com/a/10759061/3761783
import threading 
import mocp #own script

#Configuration
config = configparser.ConfigParser()
config.read_file(open('/home/pi/audiopi.cfg'))

MUSIC_BASE_DIRECTORY = config['audiopi']['MusicBaseDirectory']
SYSTEM_SOUND_DIRECTORY = config['audiopi']['SystemSoundDirectory']

SHUTDOWN_TIME = float(config['audiopi']['ShutdownTimer'])
QR_SCANNER_TIMEOUT = int(config['audiopi']['qrScannerTimeout'])
ACTIVE_TIMER = int(config['audiopi']['ActivityTimer'])

BOUNCE_TIME_SHUTDOWN = int(config['audiopi']['ButtonBounceTimeShutdown'])
BOUNCE_TIME_SCAN = int(config['audiopi']['ButtonBounceTimeScan'])
BOUNCE_TIME_TOGGLE_PLAY = int(config['audiopi']['ButtonBounceTimeTogglePlay'])
BOUNCE_TIME_NEXT = int(config['audiopi']['ButtonBounceTimeNext'])
BOUNCE_TIME_PREVIOUS = int(config['audiopi']['ButtonBounceTimePrevious'])
BOUNCE_TIME_VOLUME_UP = int(config['audiopi']['ButtonBounceTimeVolumeUp'])
BOUNCE_TIME_VOLUME_DOWN = int(config['audiopi']['ButtonBounceTimeVolumeDown'])

PIN_LED_PHOTO = int(config['audiopi']['PinLedPhoto'])
PIN_BUTTON_SCAN_PLAY = int(config['audiopi']['PinButtonScan'])
PIN_BUTTON_TOGGLE_PLAY = int(config['audiopi']['PinButtonTogglePlay'])
PIN_BUTTON_VOLUP = int(config['audiopi']['PinButtonVolUp'])
PIN_BUTTON_VOLDOWN = int(config['audiopi']['PinButtonVolDown'])
PIN_BUTTON_NEXT = int(config['audiopi']['PinButtonNext'])
PIN_BUTTON_PREVIOUS = int(config['audiopi']['PinButtonPrevious'])
PIN_BUTTON_SHUTDOWN = int(config['audiopi']['PinButtonShutdown'])

#global variables
LOOP_FOLDER_COUNTER = 0

#function for button "play/pause"
def play_pause_callback(channel):
    #reset function: loop counter
    global LOOP_FOLDER_COUNTER
    LOOP_FOLDER_COUNTER = 0
    #do main function
    mocp.toggle_play_pause()
    #reset function: title repeat
    mocp.repeat(False)


#function for button "next song"
def next_callback(channel):
    mocp.next_song()
    logging.info("TEST: "+ str(channel))

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
    global LOOP_FOLDER_COUNTER

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
            play_status = True
            
            if qr_code.startswith("cmd://"):
                #cards for music update or system update
                commands = qr_code[6:]
                #example: commands = 'ls -l /home/pi; touch /home/pi/test.txt; ls -l /home/pi; rm /home/pi/test.txt'
                logging.info("Command: "+ str(commands))
                for command in commands.split(';'):
                    subprocess.call(command.strip().split(), shell=False)
            elif qr_code.startswith("toggleOutput"):
                mocp.start_server(True)
            elif qr_code.startswith("stream://"):
                #card for streaming (radio)
                play_stream(qr_code[9:])
            elif qr_code.startswith("loop_folder://"):
                #card for loop whole folder
                loop_couter_string = qr_code[14:]
                if loop_couter_string.isnumeric():
                    LOOP_FOLDER_COUNTER = loop_couter_string
                else:
                    LOOP_FOLDER_COUNTER = 1
                logging.info("Loop folder for "+ LOOP_FOLDER_COUNTER +" times")
            elif qr_code.startswith("loop_title"):
                logging.info("Loop title")
                mocp.repeat(True)
            elif qr_code.startswith("timer://"):
                #card for setting timeout to shutdown system (sleep timer)
                seconds = qr_code[8:]
                logging.info("Set timer to "+ seconds +" seconds")
                timer = threading.Timer(int(seconds), play_fail) 
            elif qr_code != "":
                #try to play the given string
                #replace blanks with underscore
                qr_code = qr_code.replace(" ", "_")
                full_path = MUSIC_BASE_DIRECTORY + qr_code
                logging.info("full_music_path: " + full_path)
                play(full_path)
            else:
                play_status = False
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
    global LOOP_FOLDER_COUNTER

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s')
    logging.info('Initializing')

    GPIO.setwarnings(False) 
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
    GPIO.add_event_detect(PIN_BUTTON_SHUTDOWN, GPIO.FALLING, callback=shutdown_callback, bouncetime=BOUNCE_TIME_SHUTDOWN)
    GPIO.add_event_detect(PIN_BUTTON_TOGGLE_PLAY, GPIO.FALLING, callback=play_pause_callback, bouncetime=BOUNCE_TIME_TOGGLE_PLAY)
    GPIO.add_event_detect(PIN_BUTTON_VOLUP, GPIO.FALLING, callback=volup_callback, bouncetime=BOUNCE_TIME_VOLUME_UP)
    GPIO.add_event_detect(PIN_BUTTON_VOLDOWN, GPIO.FALLING, callback=voldown_callback, bouncetime=BOUNCE_TIME_VOLUME_DOWN)
    GPIO.add_event_detect(PIN_BUTTON_NEXT, GPIO.FALLING, callback=next_callback, bouncetime=BOUNCE_TIME_NEXT)
    GPIO.add_event_detect(PIN_BUTTON_PREVIOUS, GPIO.FALLING, callback=prev_callback, bouncetime=BOUNCE_TIME_PREVIOUS)
    bounce_time_for_scan = ((QR_SCANNER_TIMEOUT * 1000) + BOUNCE_TIME_SCAN) #Timeouts addieren und in ms umrechnen
    GPIO.add_event_detect(PIN_BUTTON_SCAN_PLAY, GPIO.RISING, callback=scan_and_play_callback, bouncetime=bounce_time_for_scan)

    #Start mocp server
    mocp.start_server()

    #Play "bootup sound" to show that the pi is ready to use
    title = SYSTEM_SOUND_DIRECTORY + 'boot.mp3'
    mocp.play_system_sound(title)

    shutdown_timer_running = False

    try:
        while True:
            logging.info('Waiting for activity')
            time.sleep(ACTIVE_TIMER)

            if (mocp.check_mocp_playing() == False) and (shutdown_timer_running == False):
                #check loop folder
                if LOOP_FOLDER_COUNTER > 0:
                    LOOP_FOLDER_COUNTER = LOOP_FOLDER_COUNTER - 1
                    #start playing from beginning
                    mocp.restart_playlist()
                else:
                    shutdown_timer = threading.Timer(SHUTDOWN_TIME, system_shutdown)
                    shutdown_timer.start()
                    logging.info('Shutdowntimer started!')
                    shutdown_timer_running = True
            elif (mocp.check_mocp_playing() == True) and (shutdown_timer_running == True):
                shutdown_timer.cancel()
                logging.info('Shutdowntimer canceled!')
                shutdown_timer_running = False

    #Exit when Ctrl-C is pressed
    except KeyboardInterrupt:
        logging.info('Shutdown by Ctrl-C')
        
    finally:
        logging.info('Reset GPIO configuration and close process! AudioPi says goodbye...')
        GPIO.cleanup()

#Driver Code 
if __name__ == '__main__': 
    main() 
