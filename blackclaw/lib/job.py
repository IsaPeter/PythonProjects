#!/usr/bin/env python3

class Job:
    def __init__(self):
        self.name = ''
        # A modul ebben az esetben a tényleges modul selfje
        # ami ide hozzá lesz adva annak van mindíg terminate() metódusa
        self.module = None
    def terminate(self):
        if self.module != None:
            self.module.terminate()