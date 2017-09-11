#!/usr/bin/python
import time
import os
import RPi.GPIO as GPIO
from threading import Thread, Event

class WaitColorLED():
    def __init__(self):
        self.result = 1
        self.stop_event = Event()
        
        GPIO.setmode(GPIO.BCM)

        self.GPIO17 = 17 
        self.GPIO22 = 22
        self.GPIO23 = 23
        
        GPIO.setup(self.GPIO17, GPIO.OUT)
        GPIO.setup(self.GPIO22, GPIO.OUT)
        GPIO.setup(self.GPIO23, GPIO.OUT)
        
        GPIO.output(self.GPIO17, 1)
        GPIO.output(self.GPIO23, 1)

        self.RED = GPIO.PWM(self.GPIO22, 60)
        self.RED.start(0)
            
    def FlashRed(self):
        try:
            while not self.stop_event.is_set():
                for dc in range(100, -1, -10):
                    self.RED.ChangeDutyCycle(dc)
                    time.sleep(0.1)
                    
                time.sleep(0.2)
                
                for dc in range(0, 101, 10):
                    self.RED.ChangeDutyCycle(dc)
                    time.sleep(0.1)

        except KeyboardInterrupt:
            pass

        self.stopColor()
        self.stop_event.clear()

    def setColor(self):
        th = Thread(target=self.FlashRed)
        th.setDaemon(True)
        th.start()


    def stopColor(self):
        self.RED.stop()
        GPIO.output(self.GPIO17, 0)
        GPIO.output(self.GPIO23, 0)
        GPIO.cleanup()
