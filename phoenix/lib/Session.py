#!/usr/bin/env python3
"""
Session Module
"""
import os,sys
# append base path to sys.path
runpath = os.path.dirname(os.path.realpath(__file__))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
sys.path.append(os.path.join(runpath,'..'))
sys.path.append(approot)
import lib.shm as shm



def get_current_session():
    return shm.current_session
def find_session(session_name):
    for s in shm.connected_clients:
        if s.name == session_name:
            return s
    return None
def exec_cmd(cmd,session=None):
    if session == None:
        cs = get_current_session() # got the current session
    else:
        cs = find_session(session)
    if cs:
        cs.send(cmd)
        result = cs.receive_all()
        return result.decode()
    else:
        print("[!] Session not found")
        
