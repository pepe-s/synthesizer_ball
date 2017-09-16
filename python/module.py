# -*- coding: utf-8 -*-
"""

2017.09.15 teppei

"""

from threading import Thread,Event

class Module():
    def __init__(self, name):
        self.stop_event = Event()
        self.th = None
        self.name = name

    def spin(self):
        pass

    def run(self):
        if not self.th is None:
            print "already run %s" % self.name
            return
        self.th = Thread(target=self.spin)
        self.th.setDaemon(True)
        self.th.start()

    def stop(self):
        self.stop_event.set()
        self.spi.close()
        print "%s stop" % self.name
        if not self.th is None:
            self.th.join()
            print "%s thread is stopped" % self.name