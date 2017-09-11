#!/usr/bin/python
import time
from neopixel import *
from threading import Thread, Event

LEDS        = 12     # Aantel LEDS
PIN         = 18     # GPIO 18 / PIN 12
BRIGHTNESS  = 255     # min 0 / max 255

KLEUR_R     = 200
KLEUR_G     = 0
KLEUR_B     = 0

class WaitColorRing():
    def __init__(self):
        self.result = 1
        self.stop_event = Event()
        
        self.ring = Adafruit_NeoPixel(LEDS, PIN, 800000, 5, False, BRIGHTNESS)
        self.ring.begin()

    def loopLed(self, color, wait_ms):
        try:
            while not self.stop_event.is_set():
                for i in range(self.ring.numPixels()):
                    self.ring.setPixelColor(i,color)
                    self.ring.show()
                    time.sleep(wait_ms/1000.0)
                    #self.ring.setPixelColor(i,0)

                for i in range(self.ring.numPixels()):
                    self.ring.setPixelColor(i,Color(0,0,0))
                    self.ring.show()
                    time.sleep(wait_ms/1000.0)
                    #self.ring.setPixelColor(i,0)

        except KeyboardInterrupt:
            pass

        self.resetLeds()
        self.stop_event.clear()

    def setColor(self):
        th = Thread(target=self.loopLed, args=(Color(KLEUR_G, KLEUR_R, KLEUR_B),100,))
        th.setDaemon(True)
        th.start()

    def resetLeds(self, wait_ms=10):
        for i in range(self.ring.numPixels()):
            self.ring.setPixelColor(i, Color(0,0,0))
            self.ring.show()
                
