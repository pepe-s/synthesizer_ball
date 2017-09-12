#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import signal
import os
import RPi.GPIO as GPIO
from threading import Thread, Event
import spidev

GPIO17 = 17 
GPIO22 = 22
GPIO23 = 23

class FullColorLED():
    def __init__(self, stand):
        self.stop_event = Event()
        self.th = None
        signal.signal(signal.SIGINT, self.sigStop)
        self.stand = stand
        
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(GPIO17, GPIO.OUT)
        GPIO.setup(GPIO22, GPIO.OUT)
        GPIO.setup(GPIO23, GPIO.OUT)

        self.GREEN = GPIO.PWM(GPIO17, 60)
        self.RED = GPIO.PWM(GPIO22, 60)
        self.BLUE = GPIO.PWM(GPIO23, 60)

        self.GREEN.start(0)
        self.RED.start(0)
        self.BLUE.start(0)

    def baseColor(self,val):
        # Green
        if val == 1:
            self.RED.ChangeDutyCycle(100)
            self.BLUE.ChangeDutyCycle(100)
        # Red
        elif val == 2:
            self.GREEN.ChangeDutyCycle(100)
            self.BLUE.ChangeDutyCycle(100)
        # Blue
        elif val == 3:
            self.GREEN.ChangeDutyCycle(100)
            self.RED.ChangeDutyCycle(100)
        # Yellow
        elif val == 4:
            self.BLUE.ChangeDutyCycle(100)
        # Pink
        elif val == 5:
            self.GREEN.ChangeDutyCycle(100)
        # SkyBlue
        elif val == 6:
            self.RED.ChangeDutyCycle(100)
        # White
        elif val == 7:
            pass

    def changeColor(self,val,dc):
        # Green
        if val == 1:
            self.GREEN.ChangeDutyCycle(dc)
        # Red
        elif val == 2:
            self.RED.ChangeDutyCycle(dc)
        # Blue
        elif val == 3:
            self.BLUE.ChangeDutyCycle(dc)
        # Yellow
        elif val == 4:
            self.GREEN.ChangeDutyCycle(dc)
            self.RED.ChangeDutyCycle(dc)
        # Pink
        elif val == 5:
            self.BLUE.ChangeDutyCycle(dc)
            self.RED.ChangeDutyCycle(dc)
        # SkyBlue
        elif val == 6:
            self.BLUE.ChangeDutyCycle(dc)
            self.GREEN.ChangeDutyCycle(dc)
        # White
        elif val == 7:
            self.BLUE.ChangeDutyCycle(dc)
            self.RED.ChangeDutyCycle(dc)
            self.GREEN.ChangeDutyCycle(dc)
    
    def blightED(self, color):
        for dc in range(100, -1, -10):
            self.changeColor(color,dc)
            time.sleep(0.05)

    def fadeLED(self, color):
        for dc in range(0, 101, 10):
            self.changeColor(color,dc)
            time.sleep(0.05)

    def FlashLedPWM(self,color):
        while not self.stop_event.is_set():
            if self.stand.mode == 0:
                color = 1
            elif self.stand.mode == 1:
                color = 3
            elif self.stand.mode == 2:
                color = 4
            else:
                color = 2

            self.baseColor(color)
            
            self.blightED(color)
            time.sleep(0.2)
            self.fadeLED(color)

    def run(self, color=2):
        self.th = Thread(target=self.FlashLedPWM, args=(color,))
        self.th.setDaemon(True)
        self.th.start()

    def stop(self):
        print "full color led stop"
        self.stop_event.set()
        if not self.th is None:
            self.th.join(0.5)
            print "full color led thread stopped"
        
        self.GREEN.stop()
        self.RED.stop()
        self.BLUE.stop()
        GPIO.cleanup()


    def sigStop(self, signum, frame):
        self.stop()
