# -*- coding: utf-8 -*-

from threading import Thread, Event
from time import sleep

event = Event()

def test(name, cnt):
    while not event.is_set():
        print name
        sleep(cnt)

    
if __name__ == "__main__":
    th1 = Thread(target=test, args=("testA", 0.2))
    th2 = Thread(target=test, args=("testB", 0.3))
    th1.start()
    th2.start()
    sleep(5)
    event.set()
    th1.join()
    th2.join()

        
