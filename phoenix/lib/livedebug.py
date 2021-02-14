#!/usr/bin/env python3
import os, sys
runpath = os.path.dirname(os.path.realpath(__file__))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
sys.path.append(os.path.join(runpath,'..'))
sys.path.append(approot)
import lib.shm as shm
import lib.sessionhandler as sh

prompt = "debug> "
run_debugger = True

def debugger():
    global run_debugger, prompt
    run_debugger = True
    while run_debugger:
        cmd = input(prompt)
        command_interpreter(cmd)

def command_interpreter(command):
    global run_debugger
    if command == 'exit': run_debugger = False
    if command == 'sessions': debug_sessions()
    if command == '1':get_socket_names()
    if command == '2':debug2()
    if command == 'fdtest': fdtest()
    if command == 'a':
        sessionhandler()

def debug_sessions():
    timeout = 1
    import time
    a = True
    try:
        while a:
            for s in shm.connected_clients:
                print(f"{s.name} => {str(s.check_connection_alive())} Fileno: {str(s.client.fileno())}")
            time.sleep(timeout)
    except KeyboardInterrupt:
        a = False
        
def get_socket_names():
    for s in shm.connected_clients:
        print(f"{s.name} => sockname: {s.client.getsockname()} peername:{s.client.getpeername()}")    
def debug2():
    for s in shm.connected_clients:
        for i in str(s.client).split():
            print(i)
def fdtest():
    import os,time
    for s in shm.connected_clients:
        fno = s.client.fileno()
        pid = os.getpid()
        path = f"/proc/{str(pid)}/fd/{str(fno)}"
        print(path)
        print(os.path.exists(path))
    time.sleep(1)
def sessionhandler():
    s = sh.sessionHandler(shm.connected_clients[0])
    s.interactive()
        
        