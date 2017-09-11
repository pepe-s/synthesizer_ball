# -*- coding: utf-8 -*-
"""

2017.09.11 teppei

"""

import traceback
from time import sleep
from threading import Thread, Event
from LEDctl import PWM, WaitLed, WaitRing, RunRing
import medal
from pygame import mixer
from sound import Game, SoundSE

ROHM_RAW = "D1:D7:7E:49:81:20"
SLEEP_SEC = 0.1

mode = 1


# main program
def main():
    try:
#        a = WaitLed.WaitColorLED()
#        b = WaitRing.WaitColorRing()
#        a.setColor()
#        b.setColor()

        # soud settings
        mixer.init(frequency = 48000, size = -16, channels = 2, buffer = 1024)
        se = SoundSE()
        game = Game()
        print "soud init ok"
        
        # ble connect
        sm = medal.SensorMedal(ROHM_RAW)
        print "ble connected !!"

        # notify subscribe
        sm.writeCharacteristic(0x0b07, "\x01\x00", True)
        print "write char OK"
        
#        a.stop_event.set()
#        b.stop_event.set()
#        sleep(1)
#        led = PWM.FullColorLED()
#        led.setColor(3)
#        ring = RunRing.WaitColorRing()
#        ring.setColor()
        #if a is not None:
           # a.stopColor()
        #if b is not None:
           # b.resetLeds()
        
        sm.getData()

        if mode == 1:
            while True:
                if sm.ang_x > 100:
                    se.play(0)
                if sm.ang_y > 100:
                    se.play(1)
                if sm.ang_z > 100:
                    se.play(2)
                if sm.ang_x < -100:
                    se.play(3)
                if sm.ang_y < -100:
                    se.play(4)
                if sm.ang_z < -100:
                    se.play(5)
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
                
        # if a is not None:
        #     a.stopColor()
        # if b is not None:
        #     b.resetLeds()
        # if led is not None:
        #     led.stopColor()
        # if ring is not None:
        #     ring.resetLeds()         

    except:
        traceback.print_exc()
        
    finally:
        mixer.quit()
        
        if sm is not None:
            sm.stop_event.set()
            print "getData thread is stop"
            sm.disconnect()
            
        # a.stop_event.set()
        # b.stop_event.set()
        # led.stop_event.set()
        # ring.stop_event.set()   

        # if led is not None:
        #     led.stopColor()
        # if ring is not None:
        #     ring.resetLeds()
        # if a is not None:
        #     a.stopColor()
        # if b is not None:
        #     b.resetLeds()
        
if __name__ == "__main__":
    main()
    

