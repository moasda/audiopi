import RPi.GPIO as GPIO
import time

#Configuration
PIN_LED_PHOTO = 23

#Main function
def main():
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_LED_PHOTO, GPIO.OUT, initial=GPIO.LOW)

    GPIO.output(PIN_LED_PHOTO, GPIO.HIGH)

    #Dimmer:
    #pwm = GPIO.PWM(PIN_LED_PHOTO, 100)
    #pwm.start(0)

    #for x in range(100):
        #pwm.ChangeDutyCycle(x)
        #time.sleep(0.2)

    #time.sleep(10)
    #pwm.stop()
    #GPIO.cleanup()

#Driver Code
if __name__ == '__main__':
    main()
