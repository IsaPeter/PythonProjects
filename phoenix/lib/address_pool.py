#!/usr/bin/env python3
"""
Address Pool module for Phoenix
"""
from random import randint

class addressPool():
    def __init__(self,start=5000,size=1000):
        self.address_pool = []
        self.__fill_pool(start,size)
        
    def __fill_pool(self,start,size):
        for i in range(start,start+size):
            self.address_pool.append(int(i))
    def get_address(self):
        addr = randint(self.address_pool[0],self.address_pool[len(self.address_pool)-1])
        self.address_pool.remove(addr)
        return addr
    def put_address(self,addr):
        try:
            if addr not in self.address_pool:
                self.address_pool.append(int(addr))
                self.address_pool = sorted(self.address_pool)
        except:
            pass