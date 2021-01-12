#!/usr/bin/env python3

import sys, os, socket
import shm
import tcp_client as tc

class TCPServer():
    def __init__(self,address='127.0.0.1',port=9001):
        self.server_address = address
        self.server_port = port        
        self.connected_client = None
    def listen(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.server_address, self.server_port))
            print(f"[+] Listening on {self.server_address}:{str(self.server_port)}")
            s.listen(1)
            conn, addr = s.accept()
            c = tc.TCPClient(conn,addr)
            print(f"[+] Client Connected with address {str(addr[0])} ==> {c.name}")
            shm.connected_clients.append(c)
            self.connected_client = c
            
        except Exception as x:
            print(f"[-] {x}")
    def get_client(self):
        return self.connected_client