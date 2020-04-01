#!/usr/bin/python3

import RPi.GPIO as GPIO
import logging
import time
import subprocess
import select  #for polling zbarcam, see http://stackoverflow.com/a/10759061/3761783
import threading 


#Configuration
QR_SCANNER_TIMEOUT = 4
BOUNCE_TIME = 800

PIN_LED_PHOTO = 23


#Main function
def main():
    #config root logger and add the rotation handler to the root logger
    log_handler = RotatingFileHandler(LOG_FILE, mode='a', maxBytes=5000000, backupCount=5) #5 MB
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s', handlers=[log_handler])
    logging.info('Initializing')

    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)
    #setup and turn LED on for photo
    GPIO.setup(PIN_LED_PHOTO, GPIO.OUT, initial=GPIO.HIGH)

    try:
        while True:
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
                    
                    if qr_code.startswith("cmd://"):
                        logging.info("--> do system activity")
                    elif qr_code.startswith("stream://"):
                        logging.info("--> Stream music")
                    elif qr_code.startswith("timer://"):
                        logging.info("--> Set timer")
                    elif qr_code != "":
                        logging.info("--> Play music")
                else:
                    logging.warning('Timeout on zbarcam')

            zbarcam.terminate()
            #turn LED off for photo
            GPIO.output(PIN_LED_PHOTO, GPIO.LOW)

    #Exit when Ctrl-C is pressed
    except KeyboardInterrupt:
        logging.info('Test is over')
        GPIO.cleanup()
        
    finally:
        logging.info('Test is over')
        GPIO.cleanup()

#Driver Code 
if __name__ == '__main__': 
    main() 
