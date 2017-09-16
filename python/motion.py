# -*- coding: utf-8 -*-
"""

2017.09.15 teppei

"""

from time import sleep
from module import Module

INTERVAL = 0.15

class MotionDetect(Module):
    def __init__(self, medal):
        Module.__init__("motion detect")
        self.medal = medal # use read only
        
        self.acc_x = [0.0 for i in range(5)]
        self.acc_y = [0.0 for i in range(5)]
        self.acc_z = [0.0 for i in range(5)]
        
        self.mag_x = [0.0 for i in range(5)]
        self.mag_y = [0.0 for i in range(5)]
        self.mag_z = [0.0 for i in range(5)]
        
        # none:0, roll:1, throw_weak:2, throw_strong:3, throw_verystrong:4
        self.motion = 0  

    def setData(self):
        self.acc_x.append(self.medal.acc_x)
        self.acc_x.pop(0)
        self.acc_y.append(self.medal.acc_y)
        self.acc_y.pop(0)
        self.acc_z.append(self.medal.acc_z)
        self.acc_z.pop(0)

        self.mag_x.append(self.medal.mag_x)
        self.mag_x.pop(0)
        self.mag_y.append(self.medal.mag_y)
        self.mag_y.pop(0)
        self.mag_z.append(self.medal.mag_z)
        self.mag_z.pop(0)

    def detect(self, acc, mag):
        self.motion = 0
        if mag > 30:
            self.motion = 1
        else:
            if acc > 25.0:
                self.motion = 4
            elif acc > 20.0:
                self.motion = 3
            elif acc > 15.0:
                self.motion = 2
        
    def getDiff(self)
        sub_acc = []
        sub_acc.append(abs(self.acc_x[5] - self.acc_x[4]))
        sub_acc.append(abs(self.acc_y[5] - self.acc_y[4]))
        sub_acc.append(abs(self.acc_z[5] - self.acc_z[4]))

        sub_mag = []
        sub_mag.append(abs(self.mag_x[5] - self.mag_x[4]))
        sub_mag.append(abs(self.mag_y[5] - self.mag_y[4]))
        sub_mag.append(abs(self.mag_z[5] - self.mag_z[4]))
        
        return (max(sub_acc), max(sub_mag))

    def spin(self):
        while not self.stop_event.is_set():
            self.setData()
            d_acc, d_mag = self.getDiff()
            self.detect()
            sleep(INTERVAL)