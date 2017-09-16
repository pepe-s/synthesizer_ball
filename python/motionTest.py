# -*- coding: utf-8 -*-

import traceback
from medal import SensorMedal
from pygame import mixer
from time import sleep

# ROHM_RAW = "D1:D7:7E:49:81:20"
ROHM_RAW = "E3:B0:C8:8F:A1:22"

def main():
    try:
        mixer.init(frequency = 48000, size = -16, channels = 2, buffer = 512)
        
        roll = mixer.Sound("../SE/se_soa08.wav")
        voice1 = mixer.Sound("../SE/line-girl1-line-girl1-hyaa1.wav")
        voice2 = mixer.Sound("../SE/line-girl1-line-girl1-kyaaa1.wav")
        voice3 = mixer.Sound("../SE/line-girl1-line-girl1-gyaaa1.wav")
        print "sound init"

        medal = SensorMedal(ROHM_RAW)
        # notify subscribe
        medal.writeCharacteristic(0x0b07, "\x01\x00", True)
        print "write char OK"
        medal.getData()
        print "medal run"

        while True:
            sub = abs(medal.hst_mag[1] - medal.hst_mag[0])
            if sub > 30:
                roll.play()
            else:
                x = abs(medal.hst_acc[1] - medal.hst_acc[0])
                if x >25:
                    voice3.play()
                    sleep(2)
                if x > 20:
                    voice2.play()
                    sleep(1.5)
                if x > 15:
                    voice1.play()
                    sleep(1.2)
            sleep(0.15)

    except KeyboardInterrupt:
        print "ctl - c"

    except :
        traceback.print_exc()

    finally:
        mixer.quit()
        
        if not medal is None:
            medal.stop()
            medal.disconnect()


if __name__ == "__main__":
    main()
