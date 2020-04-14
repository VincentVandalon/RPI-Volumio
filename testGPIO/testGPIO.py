#KY040 Python Class
#Martin O'Hanlon
#stuffaboutcode.com

import RPi.GPIO as GPIO
from time import sleep

class KY040:

    CLOCKWISE = 0
    ANTICLOCKWISE = 1
    
    def __init__(self, clockPin, dataPin, switchPin,
                 rotaryCallback, switchCallback):
        #persist values
        self.clockPin = clockPin
        self.dataPin = dataPin
        self.switchPin = switchPin
        self.rotaryCallback = rotaryCallback
        self.switchCallback = switchCallback
        self.commandQueue = []

        #setup pins
        GPIO.setup(clockPin,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(dataPin,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(switchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #GPIO.add_event_detect(clockPin, GPIO.RISING, bouncetime=10)
        #GPIO.add_event_detect(dataPin, GPIO.RISING, bouncetime=10)
        #GPIO.add_event_detect(switchPin, GPIO.RISING, bouncetime=10)
        while False:
            sleep(0.05)
            if GPIO.event_detected(switchPin):
                print('Trigger:'+str(switchPin))
            if GPIO.event_detected(clockPin):
                print('Trigger:'+str(clockPin) + 'other:' + str(GPIO.event_detected(dataPin)))
                #print(GPIO.input(dataPin))
            if GPIO.event_detected(dataPin):
                print('Trigger:'+str(dataPin) + 'other:' + str(GPIO.event_detected(clockPin)))

    def start(self):
        GPIO.add_event_detect(self.switchPin,
                              GPIO.RISING,
                              callback=self._genericCallback,
                              bouncetime=100)
        GPIO.add_event_detect(self.clockPin,
                              GPIO.RISING,
                              callback=self._clockCallback,
                              bouncetime=100)
        #GPIO.add_event_detect(self.dataPin,
        #                      GPIO.RISING,
        #                      callback=self._genericCallback,
        #                      bouncetime=100)

    def stop(self):
        GPIO.remove_event_detect(self.clockPin)
        GPIO.remove_event_detect(self.switchPin)
        GPIO.remove_event_detect(self.dataPin)
    
    def _genericCallback(self, pin):
        #print(str(pin) + " " + str(GPIO.input(pin)) )
        if pin == self.switchPin:
            self._switchCallback(pin)
        else:
            self.commandQueue.append(pin)
            print(self.commandQueue)

    def _clockCallback(self, pin):
        self.commandQueue.append(pin)
        #if GPIO.input(self.clockPin) == 0:
        data = (self.commandQueue[0] == self.dataPin)
        self.commandQueue = []
        data = GPIO.input(self.dataPin)

        if data == 1:
            self.rotaryCallback(self.ANTICLOCKWISE)
        else:
            self.rotaryCallback(self.CLOCKWISE)
    
    def _switchCallback(self, pin):
        #if GPIO.input(self.switchPin) == 1:
        self.switchCallback()

#test
if __name__ == "__main__":
    
    CLOCKPIN = 6
    DATAPIN = 13
    SWITCHPIN = 5

    def rotaryChange(direction):
        print "turned - " + str(direction)

    def switchPressed():
        print "button pressed"

    GPIO.setmode(GPIO.BCM)
    
    ky040 = KY040(CLOCKPIN, DATAPIN, SWITCHPIN,
                  rotaryChange, switchPressed)

    ky040.start()

    try:
        while True:
            sleep(0.1)
    finally:
        ky040.stop()
        GPIO.cleanup()
