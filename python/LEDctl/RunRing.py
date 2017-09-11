#!/usr/bin/python
import time
from neopixel import *
from threading import Thread, Event
import spidev

LEDS        = 12     # Aantel LEDS
PIN         = 18     # GPIO 18 / PIN 12
BRIGHTNESS  = 255     # min 0 / max 255

KLEUR_R     = 255
KLEUR_G     = 255
KLEUR_B     = 255

class WaitColorRing():
    def __init__(self):
        self.result = 1
        self.stop_event = Event()
        
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        
        self.ring = Adafruit_NeoPixel(LEDS, PIN, 800000, 5, False, BRIGHTNESS)
        self.ring.begin()
        
        self.vol1 = 0
        self.vol2 = 0

    def loopLed(self, color, wait_ms):
        try:
            while not self.stop_event.is_set():
                
                # ch0
                resp = self.spi.xfer2([0x68, 0x00])
                self.vol1 = (resp[0]*256+resp[1]) & 0x3ff
                if self.vol1 > 900:
                    color = Color(0, 0, 255)
                elif self.vol1 < 100:
                    color = Color(255, 255, 0)
                else:
                    color = Color(255, 0, 0)
                
                for i in range(self.ring.numPixels()):
                    self.ring.setPixelColor(i,color)
                    self.ring.show()
                    time.sleep(wait_ms/1000.0)
                    self.ring.setPixelColor(i,0)

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
                
