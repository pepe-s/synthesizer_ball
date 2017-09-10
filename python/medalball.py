# -*- coding: utf-8 -*-
"""

2017.09.09 teppei

"""
import traceback
from time import sleep, time
from threading import Thread, Event
import medal
from pygame import mixer

ROHM_RAW = "E3:B0:C8:8F:A1:22"
SE_BOUND = "../SE/byun.wav"
BGM_GAME = "../SE/gamebgm.wav"
BGM_START = "../SE/se_moa08.wav"
BGM_STOP = "../SE/se_sua02.wav"

SLEEP_SEC = 0.1 

mode = 2


class Game():
    def __init__(self):
        self.bgm = mixer.Sound(BGM_GAME)
        self.bgmstart = mixer.Sound(BGM_START)
        self.bgmstop = mixer.Sound(BGM_STOP)
        self.gaming = False
        self.time_start = 0.0
        self.time_limit = 0.0

    def gameStart(self):
        self.gaming = True
        self.bgmstart.play()
        sleep(1)
        self.bgm.play()
        self.time_limit = self.makeTime()
        self.time_start = time()
        print "Game start!! (%d sec)" % self.time_limit

    def gameStop(self):
        print "Game stop"
        self.gaming = False
        self.bgm.stop()
        sleep(0.1)
        self.bgmstop.play()
        sleep(1)
    
    def makeTime(self):
        return 20.0

    def isLimit(self):
        t = time() - self.time_start
        return self.time_limit < t
        
        
# main program
def main():
    try:
        # initialize
        mixer.init()
        pgm = mixer.Sound(SE_BOUND)
        game = Game()

        # ble connect
        sm = medal.SensorMedal(ROHM_RAW)
        print "connected !!"

        # notify subscribe
        sm.writeCharacteristic(0x0b07, "\x01\x00", True)
        print "write char OK"
        sm.getData()

        if mode == 1:
            while True:
                if sm.accel_z < -3:
                    print "bump"
                    pgm.play()
                print "accel_z: %f" % (sm.accel_z)
                sleep(SLEEP_SEC)
                    
        elif mode == 2:
            while True:
                if not game.gaming:
                    if sm.accel_z < -3.0:
                        game.gameStart()
                else:
                    if game.isLimit():
                        break
                
            if game.gaming:
                game.gameStop()
                    
                
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
            print "ble disconnected"

        
if __name__ == "__main__":
    main()
    

