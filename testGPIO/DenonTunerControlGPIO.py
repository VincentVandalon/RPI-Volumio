import RPi.GPIO as GPIO
from time import sleep
import json
import urllib


class DenonTunerGPIO:

    CLOCKWISE = 0
    ANTICLOCKWISE = 1
    
    def __init__(self, clockPin, dataPin, switchPin, offSwitch):
        #persist values
        self.clockPin = clockPin
        self.dataPin = dataPin
        self.switchPin = switchPin
        self.offSwitch = offSwitch

        #setup pins
        GPIO.setup(clockPin,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(dataPin,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(switchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(offSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def start(self):
        GPIO.add_event_detect(self.switchPin,
                              GPIO.RISING,
                              callback=self._switchCallback,
                              bouncetime=100)
        GPIO.add_event_detect(self.offSwitch,
                              GPIO.RISING,
                              callback=self._switchCallback,
                              bouncetime=100)
        GPIO.add_event_detect(self.clockPin,
                              GPIO.RISING,
                              callback=self._switchCallback,
                              bouncetime=100)

    def stop(self):
        GPIO.remove_event_detect(self.clockPin)
        GPIO.remove_event_detect(self.switchPin)
        GPIO.remove_event_detect(self.offSwitch)

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
        if pin == self.switchPin:
            volumioAPIString = 'http://192.168.1.105:3000/api/v1/commands/?cmd=toggle'
            print(json.load(urllib.urlopen(volumioAPIString)))
        if pin == self.offSwitch:
            volumioAPIString = 'http://192.168.1.105:3000/api/v1/commands/?cmd=stop'
            print(json.load(urllib.urlopen(volumioAPIString)))
        if pin == self.clockPin:
            self._clockCallback(pin)

#test
if __name__ == "__main__":
    
    CLOCKPIN = 6
    DATAPIN = 13
    SWITCHPIN = 5
    OFFSWITCH = 16


    GPIO.setmode(GPIO.BCM)
    
    denonGPIO = DenonTunerGPIO(CLOCKPIN, DATAPIN, SWITCHPIN, OFFSWITCH)

    denonGPIO.start()

    try:
        while True:
            sleep(0.1)
    finally:
        denonGPIO.stop()
        GPIO.cleanup()
