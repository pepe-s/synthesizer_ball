# -*- coding: utf-8 -*-
"""

2017.09.09 teppei

"""
import traceback
from time import sleep
from threading import Thread, Event
import medal
from pygame import mixer

ROHM_RAW = "E3:B0:C8:8F:A1:22"
SOUND1 = "../SE/byun.wav"
SLEEP_SEC = 0.1 


# play sound
def boundSound(pgm):
    pgm.play()

# main program
def main():
    try:
        # soud settings
        mixer.init()
        pgm = mixer.Sound(SOUND1)

        # ble connect
        sm = medal.SensorMedal(ROHM_RAW)
        print "connected !!"

        # notify subscribe
        sm.writeCharacteristic(0x0b07, "\x01\x00", True)
        print "write char OK"
        sm.getData()

        while True:
            if sm.accel_z < -3:
                print "bump"
                boundSound(pgm)
            print "accel_z: %f" % (sm.accel_z)
            sleep(SLEEP_SEC)
                
    except KeyboardInterrupt:
        print "ctl + c"

    except:
        traceback.print_exc()
        
    finally:
        mixer.quit()
        
        sm.stop_event.set()
        print "getData thread is stop"
        
        if sm is not None:
            sm.disconnect()

        
if __name__ == "__main__":
    main()
    

