#!/usr/bin/env python3
import sys, os
runpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runpath,'..'))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
import lib.tcp_server as server
import lib.events as event
import lib.shm as shm




info = {'name':'simple_tcp_server',
        'description':"Simple TCP Server for incoming connections",
        'Author':'Peter Isa',
        'type':'handler'}

options = {'lhost':'127.0.0.1',
           'lport':'1234'}

session_created = event.EventHook()

# 
def run():
    try:
        
        srv_address = options['lhost']
        srv_port = int(options['lport'])   
        lserver = server.MultiTCPServer(srv_address,srv_port,connections=1)
        lserver.session_created += server_session_created
        lserver.run()
        
    except Exception as x:
        print(f"[x] {x}")
    



def server_session_created(clienthandler):
    shm.add_session(clienthandler)
    session_created.fire(clienthandler)
    shm.add_computer(clienthandler.name)