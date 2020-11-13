#!/usr/bin/env python3

class ComputerInfo:
    def __init__(self,name):
        self.info = {}
        self.name = name
    def get_info(self,name):
        for n,v in self.info.items():
            if n == name:
                return v
        return None
    def set_info(self,name,value):
        if name != '' or name != None:
            self.info[name] = value
        



"""
ci = ComputerInfo()
ci.set_info('Hostname','kali')
ci.set_info('OS','Linux')
for n,v in ci.info.items():
    print(n,v)
"""

