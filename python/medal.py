"""

2017.08.31 teppei
センサメダルからデータを取得するプログラム
ハンドラでデータを表示する

"""
# -*- coding: utf-8 -*-

from btle import Peripheral
import struct
import btle
import binascii

ROHM_RAW = "E3:B0:C8:8F:A1:22"

class NtfyDelegate(btle.DefaultDelegate):
    def __init__(self, params):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        cal = binascii.b2a_hex(data)
        print "data : %s" % cal

        
class SensorMedal(Peripheral):
    def __init__(self, addr):
        Peripheral.__init__(self, addr)
        self.result = 1


def main():
    try:
        medal = SensorMedal(ROHM_RAW)
        print "connected !!"
        medal.setDelegate(NtfyDelegate(btle.DefaultDelegate))

        # notify subscribe
        medal.writeCharacteristic(0x0b07, "\x01\x00", True)
        print "write char OK"
    
        while True:
            if medal.waitForNotifications(0.2):
                continue

            print "waiting ..."
    except KeyboardInterrupt:
        medal.disconnect()

        
if __name__ == "__main__":
    main()
    

