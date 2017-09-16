# -*- coding: utf-8 -*-
"""

2017.09.16 teppei

"""

import traceback
from time import sleep
from threading import Event
from pygame import mixer
from stand import BallStand
from LEDctl.LED import FullColorLED
import medal
from sound import Game, SoundPlayer

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
        mixer.init(frequency = 22050, size = -16, channels = 2, buffer = 512)
        se = SoundPlayer()
        game = Game()
        print "soud init ok"
        
        # ble connect
        sm = medal.SensorMedal(ROHM_RAW)
        sm.getData()
        print "sensor medal run"

        # start LED color change 
        led.standby = False
        
        # start OK voice
        se.playMotion("kidou")

        cnt = 0
        while True:
            # volume setting
            if se.volume != stand.volume:
                se.volume = stand.volume
            if game.volume != stand.volume:
                game.volume = stand.volume
            
            if stand.mode == 0:
                # ? mode
                if sm.ang_x > 100 or sm.ang_y > 100 or sm.ang_z > 100:
                    se.playSE("byun_w")
                    sleep(1)
                if sm.ang_x < -100 or sm.ang_y < -100 or sm.ang_z < -100:
                    se.playSE("byun_s")
                    sleep(1)
                sleep(SLEEP_SEC)

            if stand.mode == 1:
                # music mode
                if medal.ang_x > 100:
                    se.playSE("do")
                if medal.ang_y > 100:
                    se.playSE("re")
                if medal.ang_z > 100:
                    se.playSE("mi")
                if medal.ang_x < -100:
                    se.playSE("fa")
                if medal.ang_y < -100:
                    se.playSE("so")
                if medal.ang_z < -100:
                    se.playSE("ra")
                sleep(SLEEP_SEC)

            elif stand.mode == 2:
                # motion mode
                # if m.motion == 1:
                #     se.playSE("roll")
                # elif m.motion == 2:
                #     se.playMotion("hyaa", 1.2)
                # elif m.motion == 3:
                #     se.playMotion("kyaa", 1.5)
                # elif m.motion == 4:
                #     se.playMotion("gyaa", 2.0)
                sleep(0.15)

            elif stand.mode == 3:
                # game mode
                while stand.mode == 3:
                    if not game.gaming:
                        if sm.ang_x < 100.0:
                            game.gameStart()
                    else:
                        if game.isLimit():
                            break
                    if game.volume != stand.volume:
                        game.changeVolume(stand.volume)
                    sleep(0.2)
                if game.gaming:
                    game.gameStop()
    
    except KeyboardInterrupt:
        print "Ctl - c"

    except:
        traceback.print_exc()

    finally:
        if game.gaming:
            game.gameStop()
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
    

