#!/usr/bin/env python3
"""
Upload module

This module will upload data to the remote system.
"""
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import lib.shm as shm
from lib.argumentparse import ArgumentParser

info = {'name':'upload',
        'description':'upload data to the remote system',
        'type':'post',
        'author':'Peter Isa'}

options = {'session':'',
           'target_dir':'/tmp/',
           'lfile':'',
           'rfile':'',
           'method':'linux_python'}

module_session = None

def run(*args):
    global module_session
    session_name = options['session']
    module_session = shm.get_session(session_name)    
    
    
    
# upload file with linux cat method
def linux_cat():
    pass

def linux_python():
    pass

def linux_perl():
    pass

def linux_nc():
    pass