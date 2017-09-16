# -*- coding: utf-8 -*-
"""

2017.09.11 teppei

"""

from pygame import mixer
import random
from time import time, sleep


BYUN1 = "../SE/byun_s.wav"
BYUN2 = "../SE/byun_w.wav"
BASS1 = "../SE/p_do.wav"
BASS2 = "../SE/p_re.wav"
BASS3 = "../SE/p_mi.wav"
BASS4 = "../SE/p_fa.wav"
BASS5 = "../SE/p_so.wav"
BASS6 = "../SE/p_ra.wav"
PIANO1 = "../SE/pianoA.wav"
PIANO2 = "../SE/pianoB.wav"
PIANO3 = "../SE/pianoC.wav"
PIANO4 = "../SE/pianoD.wav"
PIANO5 = "../SE/pianoE.wav"
PIANO6 = "../SE/pianoF.wav"

HYAA = "../SE/line-girl1-line-girl1-hyaa1.wav"
KYAA = "../SE/line-girl1-line-girl1-kyaaa1.wav"
GYAA = "../SE/line-girl1-line-girl1-gyaaa1.wav"
ROLL = "../SE/se_soa08.wav"

KIDOU = "../SE/info-girl1-info-girl1-kidoushimashita1.wav"

BGM_GAME1 = "../SE/gamebgm.wav"
BGM_GAME2 = "../SE/Little_Happy.wav"
BGM_START = "../SE/se_moa08.wav"
BGM_STOP = "../SE/se_sua02.wav"

class SoundPlayer():
    def __init__(self):
        self.sound = {
                    "do":mixer.Sound(BASS1),
                     "re":mixer.Sound(BASS2),
                     "mi":mixer.Sound(BASS3),
                     "fa":mixer.Sound(BASS4),
                     "so":mixer.Sound(BASS5),
                     "ra":mixer.Sound(BASS6),
                     "hyaa":mixer.Sound(HYAA),
                     "gyaa":mixer.Sound(GYAA),
                     "kyaa":mixer.Sound(KYAA),
                     "roll":mixer.Sound(ROLL),
                     "kidou":mixer.Sound(KIDOU),
                     "byun_s":mixer.Sound(BYUN1),
                     "byun_w":mixer.Sound(BYUN2),
                     "piano_a":mixer.Sound(PIANO1),
                     "piano_b":mixer.Sound(PIANO2),
                     "piano_c":mixer.Sound(PIANO3),
                     "piano_d":mixer.Sound(PIANO4),
                     "piano_e":mixer.Sound(PIANO5),
                     "piano_f":mixer.Sound(PIANO6),
                     }
        self.volume = 0.5

    # sound: str
    def playSE(self, sound):
        self.sound[sound].set_volume(self.volume)
        self.sound[sound].play()
        self.sound[sound].fadeout(500)

    # sound: str
    def playMotion(self,sound ,sleeptime=1.0):
        self.sound[sound].set_volume(self.volume)
        self.sound[sound].play()
        sleep(sleeptime)


class Game():
    def __init__(self):
        self.time_limit = 0.0
        self.bgmnum = 0
        self.gaming = False
        self.volume = 0.1
        self.bgm = [BGM_GAME1, BGM_GAME2]
        self.se = {
                    "start":mixer.Sound(BGM_START),
                    "stop":mixer.Sound(BGM_STOP),
                    }

    def changeVolume(self, volume=0.5):
        self.volume = volume
        mixer.music.set_volume(volume)

    def gameStart(self):
        bgmnum = random.randint(0,1)
        self.time_limit = self.makeTime()
        self.gaming = True

        self.se["start"].set_volume(self.volume)
        self.se["start"].play()
        sleep(1)

        mixer.music.load(self.bgm[bgmnum])
        mixer.music.set_volume(self.volume)
        mixer.music.play()

        print "Game start!! (%d sec)" % self.time_limit

    def gameStop(self):
        if not self.gaming:
            print "not gaming"
            return

        print "Game stop"
        self.gaming = False
        mixer.music.stop()
        sleep(0.1)

        self.se["stop"].set_volume(self.volume)
        self.se["stop"].play()
        sleep(1)
    
    def makeTime(self):
        return random.uniform(20,80)

    def isLimit(self):
        return (mixer.music.get_pos() / 1000.0) > self.time_limit
