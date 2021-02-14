#!/usr/bin/env python3
"""
Command Interpreter modules for Prhoenix
"""
import sys, os
runpath = os.path.dirname(os.path.realpath(__file__))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
sys.path.append(os.path.join(runpath,'..'))
sys.path.append(approot)

class phoenixCommandInterpreter():
    def __init__(self,instance):
        self.instance = instance
    def run(self,command):
        if command == "list modules": # list modules
            pass
        elif command.startswith("use"): # using a module
            pass
        elif command == "help":
            pass
    