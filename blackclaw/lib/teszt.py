#!/usr/share/env python3

import os, sys
# Get the file current run path
runpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runpath,'..'))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
import lib.tcp_server as server

def sc(clienthandler):
    print(clienthandler.name)

s = server.MultiTCPServer(connections=2)
s.session_created +=sc
s.run()

print(f"Connections: {s.connected_clinets}")
