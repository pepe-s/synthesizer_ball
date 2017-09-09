# -*- coding: utf-8 -*-
"""

2017.09.09 teppei
SensorMedal Class

"""

from bluepy.btle import Peripheral
import bluepy.btle as btle
import binascii
from threading import Thread, Event

# 16
def s16(val):
    return -(val & 0b1000000000000000) | (val & 0b0111111111111111)
        
        
class SensorMedal(Peripheral):
    def __init__(self, addr):
        Peripheral.__init__(self, addr, addrType="random")
        self.result = 1
        self.stop_event = Event()
        
        self.accel_x = 0.0
        self.accel_y = 0.0
        self.accel_z = 0.0

        self.mag_x = 0.0
        self.mag_y = 0.0
        self.mag_z = 0.0
        
        self.ang_x = 0.0
        self.ang_y = 0.0
        self.ang_z = 0.0

        self.press = 0.0

    # 
    def splitData(self, raw_data):
        cnt = 0
        datas = []
        # 
        lst = [raw_data[i: i+4] for i in range(0, len(raw_data), 4)]
        for e in lst:
            # 
            lst[cnt] = lst[cnt][2:] + lst[cnt][:2]
            datas.append(int(lst[cnt], 16))
            cnt += 1
        return datas

    def calcAccel(self, val):
        return val / 1024.0 * 9.8

    def calcMag(self, val):
        return val / 10.0

    def calcAngular(self, val):
        return val / 131.0

    def calcPress(self, val):
        return val + 50000

    def printData(self):
        print self.accel_x, self.accel_y, self.accel_z, self.mag_x, self.mag_y, self.mag_z, self.ang_x, self.ang_y, self.ang_z, self.press
    
    # 
    def setDatas(self, datas):
        self.accel_x = self.calcAccel(s16(datas[0]))
        self.accel_y = self.calcAccel(s16(datas[1]))
        self.accel_z = self.calcAccel(s16(datas[2]))

        self.mag_x = self.calcMag(s16(datas[3]))
        self.mag_y = self.calcMag(s16(datas[4]))
        self.mag_z = self.calcMag(s16(datas[5]))

        self.ang_x = self.calcAngular(s16(datas[6]))
        self.ang_y = self.calcAngular(s16(datas[7]))
        self.ang_z = self.calcAngular(s16(datas[8]))

        self.press = self.calcPress(datas[9])

    # 
    def _getResp(self, wantType, timeout=None):
        if isinstance(wantType, list) is not True:
            wantType = [wantType]

        while True:
            resp = self._waitResp(wantType + ['ntfy', 'ind'], timeout)
            if resp is None:
                return None

            respType = resp['rsp'][0]
            if respType == 'ntfy' or respType == 'ind':
                hnd = resp['hnd'][0]
                data = resp['d'][0]

                datas = self.splitData(binascii.b2a_hex(data))
                self.setDatas(datas)
                
                if self.delegate is not None:
                    self.delegate.handleNotification(hnd, data)
                if respType not in wantType:
                    continue
            return resp
        
    # getData loop
    def getDataSpin(self, timeout):
        while not self.stop_event.is_set():
            if self.waitForNotifications(timeout):
                continue
        self.stop_event.clear()

    def getData(self, timeout=1.0):
        th = Thread(target=self.getDataSpin, args=(timeout,))
        th.setDaemon(True)
        th.start()
