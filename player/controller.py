import time
import subprocess
import select  # for polling zbarcam, see http://stackoverflow.com/a/10759061/3761783

#Configuration
QR_SCANNER_TIMEOUT = 4

try:
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

        zbarcam.terminate()

# Exit when Ctrl-C is pressed
except KeyboardInterrupt:
    logging.info('Shutdown')
    print("Shutdown")
    
finally:
    logging.info('Reset GPIO configuration and close')
    print("Reset GPIO configuration and close")
#    GPIO.cleanup()            