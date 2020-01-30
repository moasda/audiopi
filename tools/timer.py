import threading 
import time
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s')

# def gfg(var): 
#     print("This is the output of the timer event!!!! :) " + var) 

# print("Output before timer starts with 5 sek.\n")   
# timer = threading.Timer(5.0, gfg, ['test']) 
# timer.start()
# print("Output after timer start.\n") 

class Timer:
    #def __init__(self):
        #self.timer = ''

    def start(self, seconds):
        #self.timer = threading.Timer(seconds, self.action)
        t = threading.Timer(10, self.action) 
        if t.is_alive() == True:
            logging.debug('starting timer')
            t = threading.Timer(2.0, self.action) 
        else:
            logging.debug("running") 

    def cancel(self):
        logging.debug("cancel") 
        #self.timer.cancel()

    def action(self):
        logging.debug("This is the output of the timer event!") 


myTimer = Timer()
myTimer.start(1.0)
logging.debug("now something happens")
time.sleep(5.0)
