#KY040 Python Class
#Martin O'Hanlon
#stuffaboutcode.com

import RPi.GPIO as GPIO
from time import sleep

class KY040:

    CLOCKWISE = 0
    ANTICLOCKWISE = 1
    
    def __init__(self, clockPin, dataPin, switchPin, redLED,
                 rotaryCallback, switchCallback):
        #persist values
        self.clockPin = clockPin
        self.dataPin = dataPin
        self.switchPin = switchPin
        self.rotaryCallback = rotaryCallback
        self.switchCallback = switchCallback

        #setup pins
        GPIO.setup(clockPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(dataPin, GPIO.IN)#, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(switchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.setup(redLED, GPIO.OUT)
	GPIO.output(redLED,GPIO.HIGH)

    def start(self):
        GPIO.add_event_detect(self.clockPin,
                              GPIO.FALLING,
                              callback=self._clockCallback,
                              bouncetime=250)
        GPIO.add_event_detect(self.switchPin,
                              GPIO.FALLING,
                              callback=self._switchCallback,
                              bouncetime=250)
        #GPIO.add_event_detect(self.switchPin,
                              #GPIO.FALLING,
                              #callback=self._genericCallback,
                              #bouncetime=300)

    def stop(self):
        GPIO.remove_event_detect(self.clockPin)
        GPIO.remove_event_detect(self.switchPin)
    
    def _genericCallback(self, pin):
        print(str(pin) + " " + str(GPIO.input(pin)) )

    def _clockCallback(self, pin):
        if GPIO.input(self.clockPin) == 0:
            data = GPIO.input(self.dataPin)
            if data == 1:
                self.rotaryCallback(self.ANTICLOCKWISE)
            else:
                self.rotaryCallback(self.CLOCKWISE)
    
    def _switchCallback(self, pin):
        if GPIO.input(self.switchPin) == 1:
            self.switchCallback()

#test
if __name__ == "__main__":
    
    CLOCKPIN = 6
    DATAPIN = 13
    SWITCHPIN = 5
    REDLED = 26

    def rotaryChange(direction):
	GPIO.output(REDLED,not bool(GPIO.input(REDLED)))
        print "turned - " + str(direction)

    def switchPressed():
        print "button pressed"

    GPIO.setmode(GPIO.BCM)
    
    ky040 = KY040(CLOCKPIN, DATAPIN, SWITCHPIN, REDLED,
                  rotaryChange, switchPressed)

    ky040.start()

    try:
        while True:
            sleep(0.1)
    finally:
        ky040.stop()
        GPIO.cleanup()
