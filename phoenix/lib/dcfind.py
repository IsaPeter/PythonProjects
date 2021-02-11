#!/usr/bin/env python3

import os, sys
runpath = os.path.dirname(os.path.realpath(__file__))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
sys.path.append(os.path.join(runpath,'..'))
sys.path.append(approot)
import lib.shm as shm
import threading, time


class dead_connection_finder():
    def __init__(self):
        self.timeout = 1
        self.dowork = True
        self.work_thread = None
    def start(self):
        self.dowork = True
        self.work_thread = threading.Thread(target=self.__dowork)
        self.work_thread.start()
    def stop(self):
        self.dowork = False
        self.work_thread.join()
    def __dowork(self):
        while self.dowork:
            if len(shm.connected_clients) > 0:
                for s in shm.connected_clients:
                    if s.check_connection_alive() == False:
                        shm.connected_clients.remove(s)
                        print(f"[*] The Session with name {s.name} is dead!")
            time.sleep(self.timeout)