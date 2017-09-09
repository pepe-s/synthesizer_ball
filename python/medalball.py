# -*- coding: utf-8 -*-
"""

2017.09.09 teppei

"""
import medal

ROHM_RAW = "E3:B0:C8:8F:A1:22"

def main():
    try:
        sm = medal.SensorMedal(ROHM_RAW)
        print "connected !!"

        # notify subscribe
        sm.writeCharacteristic(0x0b07, "\x01\x00", True)
        print "write char OK"

        cnt = 0
        i = 0
        while True:
            if sm.waitForNotifications(1.0):
                sm.printData()
                continue
            
            print "waiting ..."
            
    except KeyboardInterrupt:
        pass
        
    finally:
        if sm is not None:
            sm.disconnect()
        
if __name__ == "__main__":
    main()
    

