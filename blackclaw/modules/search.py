#!/usr/bin/env python3
"""
The System Info Gathering Module

This module will gather information about the system
"""
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import lib.shm as shm
from lib.argumentparse import ArgumentParser


info = {'name':'search',
        'description':'Search in the target system',
        'type':'post',
        'author':'Peter Isa'}

options = {'session':''}

module_session = None

def run(*args):
    global module_session
    session_name = options['session']
    
    module_session = shm.get_session(session_name)
    
    # Search
    if module_session != None:    
        p = args[0].split(' ')
        if len(p) == 1:
            print("[!] Search Module need an argument!")
        else:
            word = p[1]
            payload = 'find / -type f -name "'+word+'" 2>/dev/null -exec ls -tlah {} \;'
            #print(payload)
            module_session.run_command(payload)
    
    