# -*- coding: utf-8 -*-
"""

2017.09.11 teppei

"""

from time import sleep
from threading import Thread, Event
import spidev
import signal


class BallStand():
    def __init__(self):
        self.stop_event = Event()
        self.th = None
        signal.signal(signal.SIGINT, self.sigStop)
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        
        self.volume_mode = 0
        self.volume_mixer = 0
        self.mode = 0

    def setMode(self):
        if self.volume_mode > 900:
            self.mode = 0
        elif self.volume_mode < 100:
            self.mode = 1
        else:
            self.mode = 2

    def spin(self):
        while not self.stop_event.is_set():
            resp = self.spi.xfer2([0x68, 0x00])
            self.volume_mode = (resp[0]*256+resp[1]) & 0x3ff
            self.setMode()
            print self.volume_mode
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

    def sigStop(self, signum, frame):
        self.stop()
