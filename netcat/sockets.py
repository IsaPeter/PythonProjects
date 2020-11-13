#!/usr/bin/env pythion3
import socket

RHOST = '127.0.0.1'
RPORT = 4545

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((RHOST,RPORT))

while True:
    cmd = input("shell > ")
    s.send((cmd+"\n").encode())   
    recv_len = 1
    response = b''    
    while recv_len:
        data = s.recv(100)
        response += data
        recv_len = len(data)
        print(response)
        if recv_len < 100:
            recv_len = 0
            break
        
    print(response.decode())