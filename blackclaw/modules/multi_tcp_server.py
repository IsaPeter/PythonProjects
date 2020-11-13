#!/usr/bin/env python3
import sys, os
runpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runpath,'..'))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
import lib.tcp_server as server
import lib.events as event
import lib.shm as shm
from threading import Thread
import lib.job as job



info = {'name':'multi_tcp_server',
        'description':'Handle multiple incoming connections to same port',
        'Author':'Peter Isa',
        'type':'handler'}

options = {'lhost':'127.0.0.1',
           'lport':'1234',
           'number':5,
           'threaded': 'true'}

session_created = event.EventHook()
job_started = event.EventHook()
lserver = None
server_thread = None

def run(*args):
    global lserver,server_thread
    try:
        srv_address = options['lhost']
        srv_port = int(options['lport'])
        srv_conn = int(options['number'])
        lserver = server.MultiTCPServer(srv_address,srv_port,connections=srv_conn)
        lserver.session_created += server_session_created
        
        if options['threaded'].lower() == 'true':
            server_thread = Thread(target = lserver.run) 
            server_thread.start()
            
        else:
            lserver.run()
        	
        
    except Exception as x:
        print(f"[x] {x}")
    


def terminate():
    global lserver,server_thread
    lserver.keep_running = False
    server_thread.join()

def server_session_created(clienthandler):
    shm.add_session(clienthandler)
    session_created.fire(clienthandler)