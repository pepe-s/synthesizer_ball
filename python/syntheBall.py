# -*- coding: utf-8 -*-
"""

2017.09.12 teppei

"""

import traceback
from time import sleep
from threading import Event
from pygame import mixer
from stand import BallStand
from LEDctl.LED import FullColorLED
import medal
from sound import Game, SoundSE

ROHM_RAW = "D1:D7:7E:49:81:20"
SLEEP_SEC = 0.1


# main program
def main():
    try:
        # LED settings
        stand = BallStand()
        stand.run()
        print "stand run"

        led = FullColorLED(stand)
        led.run()
        print "led run"

        # soud settings
        mixer.init(frequency = 48000, size = -16, channels = 2, buffer = 512)
        se = SoundSE()
        game = Game()
        print "soud init ok"
        
        # ble connect
        sm = medal.SensorMedal(ROHM_RAW)
        print "ble connected !!"

        # notify subscribe
        sm.writeCharacteristic(0x0b07, "\x01\x00", True)
        print "write char OK"
        sm.getData()

        # start LED color change 
        led.standby = False

        cnt = 0
        while True:
            if stand.mode == 1:
                # music mode
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
                    
            elif stand.mode == 2:
                # game mode
                while stand.mode == 2:
                    if not game.gaming:
                        if sm.accel_z < -3.0:
                            game.gameStart()
                    else:
                        if game.isLimit():
                            break
                
                if game.gaming:
                    game.gameStop()
            else:
                print "none mode %d" % cnt
                cnt += 1
                sleep(0.5)
    
    except KeyboardInterrupt:
        print "Ctl - c"

    except:
        traceback.print_exc()

    finally:
        mixer.quit()
        
        if not led is None:
            led.stop()
            print "led is stopped"
        
        if not stand is None:
            stand.stop()
            print "stand is stopped"

        if not sm is None:
            sm.stop()
            print "getData thread is stop"
            sm.disconnect()

if __name__ == "__main__":
    main()
    

