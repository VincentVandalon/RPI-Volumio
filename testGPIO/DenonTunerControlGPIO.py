import RPi.GPIO as GPIO
from time import sleep
import json
import urllib


class DenonTunerGPIO:

    CLOCKWISE = 0
    ANTICLOCKWISE = 1
    
    def __init__(self, clockPin, dataPin, switchPin):
        #persist values
        self.clockPin = clockPin
        self.dataPin = dataPin
        self.switchPin = switchPin

        #setup pins
        GPIO.setup(clockPin,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(dataPin,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(switchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
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
                              callback=self._switchCallback,
                              bouncetime=100)
        GPIO.add_event_detect(self.clockPin,
                              GPIO.RISING,
                              callback=self._clockCallback,
                              bouncetime=100)

    def stop(self):
        GPIO.remove_event_detect(self.clockPin)
        GPIO.remove_event_detect(self.switchPin)

    def _clockCallback(self, pin):
        #if GPIO.input(self.clockPin) == 0:
        data = GPIO.input(self.dataPin)

        if data == 1:
            volumioAPIString = 'http://192.168.1.105:3000/api/v1/commands/?cmd=next'
            print('up')
        else:
            volumioAPIString = 'http://192.168.1.105:3000/api/v1/commands/?cmd=prev'
            print('down')
        print(json.load(urllib.urlopen(volumioAPIString)))
    
    def _switchCallback(self, pin):
        #if GPIO.input(self.switchPin) == 1:
        volumioAPIString = 'http://192.168.1.105:3000/api/v1/commands/?cmd=toggle'
        print(json.load(urllib.urlopen(volumioAPIString)))

#test
if __name__ == "__main__":
    
    CLOCKPIN = 6
    DATAPIN = 13
    SWITCHPIN = 5


    GPIO.setmode(GPIO.BCM)
    
    denonGPIO = DenonTunerGPIO(CLOCKPIN, DATAPIN, SWITCHPIN)

    denonGPIO.start()

    try:
        while True:
            sleep(0.1)
    finally:
        denonGPIO.stop()
        GPIO.cleanup()
