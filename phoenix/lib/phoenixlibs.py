#!/usr/bin/env python3

import os,sys
# append base path to sys.path
runpath = os.path.dirname(os.path.realpath(__file__))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
sys.path.append(os.path.join(runpath,'..'))
sys.path.append(approot)
import lib.shm as shm


class RunModule():
    def __init__(self,module_name):
        self.name = module_name
        self.module = self.__get_module()
    def __get_module(self):
        for m in shm.loaded_modules:
            if m.module_id == self.name:
                return m
    def run(self,args=''):
        if self.module:
            return self.module.run(args)