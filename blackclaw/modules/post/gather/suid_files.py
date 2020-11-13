#!/usr/bin/enc python3
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import lib.shm as shm


info = {'name':'suid_finder',
        'description': 'Find SUID files in the target machine',
        'type':'post'}

options = {'session': ''}



module_session = None


def run(*args):
    global module_session
    session_name = options['session']
    payload = 'find / -type f -perm -u=s 2>/dev/null'
    has_error = False
    
    if module_session == None:
        s = get_session(session_name)
        if s != None:
            module_session = s
        else:
            has_error = True
            print("[x] Session cannot be null!")
    
    
    if has_error == False:
        if module_session.check_session_alive():
            print(f"[*] Searching SUID files..")
            module_session.run_command(payload)

def get_session(name):
    for s in shm.sessions:
        if s.name == name:
            return s
    return None


def set_session(clienthandler):
    global module_session
    module_session = clienthandler
