#!/usr/bin/python3

import RPi.GPIO as GPIO
import logging
import time
import subprocess
import select  #for polling zbarcam, see http://stackoverflow.com/a/10759061/3761783
import threading 

#Configuration
QR_SCANNER_TIMEOUT = 4
PIN_LED_PHOTO = 23

#Main function
def main():
    #config root logger and add the rotation handler to the root logger
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s')
    logging.info('Initializing')

    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)
    #setup and turn LED on for photo
    GPIO.setup(PIN_LED_PHOTO, GPIO.OUT, initial=GPIO.HIGH)

    logging.info('Start scanning')
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
                        break
                    elif qr_code.startswith("stream://"):
                        logging.info("--> Stream music")
                        url = qr_code[9:]
                        break
                    elif qr_code.startswith("timer://"):
                        logging.info("--> Set timer")
                        break
                    elif qr_code != "":
                        logging.info("--> Play music")
                        break
                else:
                    logging.warning('Timeout on zbarcam')

            time.sleep(0.5)
            zbarcam.terminate()

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
