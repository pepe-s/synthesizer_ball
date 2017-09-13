# -*- coding: utf-8 -*-

from time import sleep
from stand import BallStand
from LEDctl.LED import RingLED

try:
    stand = BallStand()
    stand.run()
    print "stand run"

    ring = RingLED(stand)
    ring.run()
    print "ring run"

    sleep(15)

except KeyboardInterrupt:
    print "ctl - c"

finally:
    ring.stop()
    stand.stop()
    