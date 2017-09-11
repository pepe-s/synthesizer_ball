#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os
import RPi.GPIO as GPIO
from threading import Thread, Event
import spidev

class FullColorLED():
    def __init__(self):
        self.result = 1
        self.stop_event = Event()
        
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        
        GPIO.setmode(GPIO.BCM)

        GPIO17 = 17 
        GPIO22 = 22
        GPIO23 = 23
        
        GPIO.setup(GPIO17, GPIO.OUT)
        GPIO.setup(GPIO22, GPIO.OUT)
        GPIO.setup(GPIO23, GPIO.OUT)

        self.GREEN = GPIO.PWM(GPIO17, 60)
        self.RED = GPIO.PWM(GPIO22, 60)
        self.BLUE = GPIO.PWM(GPIO23, 60)

        self.GREEN.start(0)
        self.RED.start(0)
        self.BLUE.start(0)
        
        self.vol1 = 0
        self.vol2 = 0

    def voltageToTemperature(self, volt):
        offset = (0.6 / 5) * 1024
        base_temp = 5 / 1024.0

        return (float)(volt - offset) * base_temp * 100.0

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
            
    def FlashLedPWM(self,color):
        try:
            while not self.stop_event.is_set():
                
                # ch0
                resp = self.spi.xfer2([0x68, 0x00])
                self.vol1 = (resp[0]*256+resp[1]) & 0x3ff
                #print self.vol1
                if self.vol1 > 900:
                    color = 3
                elif self.vol1 < 100:
                    color = 4
                else:
                    color = 1
                    
                # ch1
                #resp = self.spi.xfer2([0x78, 0x00])
                #self.vol2 = (resp[0]*256+resp[1]) & 0x3ff
                #print self.vol2
                
                self.baseColor(color)
                
                for dc in range(100, -1, -10):
                    self.changeColor(color,dc)
                    time.sleep(0.1)
                    
                time.sleep(0.2)
                
                for dc in range(0, 101, 10):
                    self.changeColor(color,dc)
                    time.sleep(0.1)

        except KeyboardInterrupt:
            pass

        self.stopColor()

        self.stop_event.clear()

    def setColor(self, color=2):
        th = Thread(target=self.FlashLedPWM, args=(color,))
        th.setDaemon(True)
        th.start()


    def stopColor(self):
        self.GREEN.stop()
        self.RED.stop()
        self.BLUE.stop()

        GPIO.cleanup()
        self.spi.close()
