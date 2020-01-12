import RPi.GPIO as GPIO
import time

#Configuration
PIN_LED_PHOTO = 23

#Main function
def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_LED_PHOTO, GPIO.OUT, initial=GPIO.LOW)

    GPIO.output(PIN_LED_PHOTO, GPIO.LOW)

#Driver Code
if __name__ == '__main__':
    main()
