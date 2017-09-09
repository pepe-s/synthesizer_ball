# -*- coding: utf-8 -*-

from btle import Peripheral
import struct
import btle
import binascii
import pygame.mixer
import time
import threading

ROHM_RAW = "D1:D7:7E:49:81:20 random"

# 16進数を符号付きで変換する
def s16(val):
    return -(val & 0b1000000000000000) | (val & 0b0111111111111111)

class NtfyDelegate(btle.DefaultDelegate):
    def __init__(self, params):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        cal = binascii.b2a_hex(data)
        # print "data : %s" % cal
        
class SensorMedal(Peripheral):
    def __init__(self, addr):
        Peripheral.__init__(self, addr)
        self.result = 1

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

    # センサメダルの生データの値を切り分ける
    def splitData(self, raw_data):
        cnt = 0
        datas = []
    # 2バイトずつにする
        lst = [raw_data[i: i+4] for i in range(0, len(raw_data), 4)]
        for e in lst:
            # 上位と下位バイトを入れ替えて変換
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

# データを変数にセット
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

    # notifyを受け取る(オーバーライド)
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

                    if self.accel_x > 10:
                        p_1G=threading.Thread(target=play1G, name="p_1G", args=(1,))
                        p_1G.start()
                    elif self.accel_y > 10:
                        p_1f=threading.Thread(target=play1G, name="p_1f", args=(2,))
                        p_1f.start()
                    elif self.accel_z > 10:
                        p_1c=threading.Thread(target=play1G, name="p_1c", args=(3,))
                        p_1c.start()

                    # self.printData()
    
                    if self.delegate is not None:
                            self.delegate.handleNotification(hnd, data)
                    if respType not in wantType:
                            continue
            return resp

def play1G(a):
    if a == 1:
        p1G.play()    
    elif a ==2:
        p1f.play()
    elif a==3:
        p1c.play()    
    
def main():
    try:

        medal = SensorMedal(ROHM_RAW)
        print "connected !!"
        medal.setDelegate(NtfyDelegate(btle.DefaultDelegate))

        # notify subscribe
        medal.writeCharacteristic(0x0b07, "\x01\x00", True)
        print "write char OK"

        cnt = 0

        while True:
                if medal.waitForNotifications(1.0):
                        continue

                print "waiting ..."
                cnt += 1
                if cnt > 1000:
                        break
        
    except KeyboardInterrupt:
        pass
    
    finally:
        medal.disconnect()
        
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.quit()
    pygame.mixer.init()

    p1G = pygame.mixer.Sound('/home/pi/bluepy/bluepy/data/1G.wav')
    p1f = pygame.mixer.Sound('/home/pi/bluepy/bluepy/data/1f.wav')
    p1c = pygame.mixer.Sound('/home/pi/bluepy/bluepy/data/1c.wav')
    
    main()

