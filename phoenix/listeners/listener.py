#!/usr/bin/env python3
import os,sys
# append base path to sys.path
runpath = os.path.dirname(os.path.realpath(__file__))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
sys.path.append(os.path.join(runpath,'..'))
sys.path.append(approot)
import lib.tcp_server as ts
import lib.shm as shm


module_name ="TCP Listener"
module_id = "listener/tcp_listener"
module_description="Listening for incoming connections"
module_type = 'listener'
variables = {'lhost':'0.0.0.0',
             'lport':'9002',
             'type':'reverse_python',
             'verbose':'true'}


def run(arguments=''):
    lhost = variables['lhost']
    lport = int(variables['lport'])
    
    TS = ts.TCPServer(address=lhost,port=lport)
    TS.listen()
    client = TS.get_client()
    if client:
        shm.connected_clients.append(client)
        
