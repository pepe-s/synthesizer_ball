# -*- coding: utf-8 -*-
"""

2017.09.11 teppei

"""

from pygame import mixer
import random
from time import time, sleep

SOUND1 = "../SE/byun.wav"
BASS1 = "../SE/p_do.wav"
BASS2 = "../SE/p_re.wav"
BASS3 = "../SE/p_mi.wav"
BASS4 = "../SE/p_fa.wav"
BASS5 = "../SE/p_so.wav"
BASS6 = "../SE/p_ra.wav"

BGM_GAME1 = "../SE/gamebgm.wav"
BGM_GAME2 = "../SE/Little_Happy.wav"
BGM_START = "../SE/se_moa08.wav"
BGM_STOP = "../SE/se_sua02.wav"


class SoundSE():
    def __init__(self):
        p1 = mixer.Sound(BASS1)
        p2 = mixer.Sound(BASS2)
        p3 = mixer.Sound(BASS3)
        p4 = mixer.Sound(BASS4)
        p5 = mixer.Sound(BASS5)
        p6 = mixer.Sound(BASS6)
        self.se = (p1, p2, p3, p4, p5, p6)
        
    # play sound
    def play(self, num):
        if num < len(self.se):
            self.se[num].play()
            self.se[num].fadeout(500)


class Game():
    def __init__(self):
        self.bgm = []
        self.bgm.append(mixer.Sound(BGM_GAME1))
        self.bgm.append(mixer.Sound(BGM_GAME2))
        self.bgmstart = mixer.Sound(BGM_START)
        self.bgmstop = mixer.Sound(BGM_STOP)
        self.gaming = False
        self.time_start = 0.0
        self.time_limit = 0.0
        self.bgmnum = 0

    def gameStart(self):
        self.bgmnum = random.randint(0,1)
        self.gaming = True

        self.bgmstart.play()
        sleep(1)
        self.bgm[self.bgmnum].play()
        
        self.time_limit = self.makeTime()
        self.time_start = time()
        print "Game start!! (%d sec)" % self.time_limit

    def gameStop(self):
        print "Game stop"
        self.gaming = False
        self.bgm[self.bgmnum].stop()
        sleep(0.1)
        self.bgmstop.play()
        sleep(1)
    
    def makeTime(self):
        return random.uniform(20,80)

    def isLimit(self):
        t = time() - self.time_start
        return self.time_limit < t
