# -*- coding: utf-8 -*-
"""

2017.09.11 teppei

"""

from time import sleep
from threading import Thread, Event
import spidev


class BallStand():
    def __init__(self):
        self.stop_event = Event()
        self.th = None
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        
        self.volume_mode = 0
        self.volume_size = 0
        self.mode = 0
        self.volume = 0.0

    def setMode(self):
        interval = 250
        a = self.volume_mode / interval
        if a >= 4:
            a = 3
        self.mode = a

    def setSize(self):
        interval = 100
        self.volume = (self.volume_size / interval) / 10.0 + 0.1
        if self.volume > 1.0:
            self.volume = 1.0

    def spin(self):
        while not self.stop_event.is_set():
            resp = self.spi.xfer2([0x78, 0x00])
            self.volume_mode = (resp[0]*256+resp[1]) & 0x3ff
            self.setMode()

            resp = self.spi.xfer2([0x68, 0x00])
            self.volume_size = (resp[0]*256+resp[1]) & 0x3ff
            self.setSize()
            sleep(0.2)

    def run(self):
        self.th = Thread(target=self.spin)
        self.th.setDaemon(True)
        self.th.start()

    def stop(self):
        self.stop_event.set()
        self.spi.close()
        print "ball stand stop"
        if not self.th is None:
            self.th.join(0.5)
            print "ball stand thread is stopped"