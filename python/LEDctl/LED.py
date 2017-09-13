#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import sleep
import RPi.GPIO as GPIO
from threading import Thread, Event
from neopixel import *

# for FullColorLED
GPIO17 = 17 
GPIO22 = 22
GPIO23 = 23

# for Ring LED
LEDS        = 12     # Aantel LEDS
PIN         = 18     # GPIO 18 / PIN 12
BRIGHTNESS  = 200     # min 0 / max 255

KLEUR_R     = 255
KLEUR_G     = 255
KLEUR_B     = 255
RING_WAIT = 1.0

class FullColorLED():
    def __init__(self, stand):
        self.stop_event = Event()
        self.th = None
        self.stand = stand      # BallStand instance
        self.standby = True     # standby mode
        
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
            sleep(0.05)

    def fadeLED(self, color):
        for dc in range(0, 101, 10):
            self.changeColor(color,dc)
            sleep(0.05)

    def spin(self):
        while not self.stop_event.is_set():
            if self.standby:
                color = 2
            else:
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
            sleep(0.1)
            self.fadeLED(color)

    def run(self):
        self.th = Thread(target=self.spin)
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

class RingLED():
    def __init__(self, stand):
        self.stop_event = Event()
        self.th = None
        self.stand = stand  # BallStand instance(read only)

        self.ring = Adafruit_NeoPixel(LEDS, PIN, 800000, 5, False, BRIGHTNESS)
        self.ring.begin()

        self.standby = True

    def blightLED(self, color):
        for i in range(self.ring.numPixels()):
            self.ring.setPixelColor(i,color)
            self.ring.show()
            sleep(RING_WAIT)
            self.ring.setPixelColor(i,0)

    def resetLeds(self):
        for i in range(self.ring.numPixels()):
            self.ring.setPixelColor(i, Color(0,0,0))
            self.ring.show()

    def spin(self):
        while not self.stop_event.is_set():

            if self.standby:
                color = Color(255,0,0)
            else:
                if self.stand.mode == 0:
                    color = Color(0, 0, 255)
                elif self.stand.mode == 1:
                    color = Color(255, 255, 0)
                elif self.stand.mode == 2:
                    color = Color(0, 255, 0)
                else:
                    color = Color(255, 0, 0)
            
            self.blightLED(color)
                
        self.resetLeds()

    def run(self):
        self.th = Thread(target=self.spin)
        self.th.setDaemon(True)
        self.th.start()
        
    def stop(self):
        print "Ring led stop"
        self.stop_event.set()
        if not self.th is None:
            self.th.join(0.5)
            print "Ring LED thread stopped"