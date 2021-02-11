#!/usr/bin/env python3

import socket, string, random, os, sys
runpath = os.path.dirname(os.path.realpath(__file__))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
sys.path.append(os.path.join(runpath,'..'))
sys.path.append(approot)
import lib.shell as shell
import lib.shm as shm

class TCPClient():
    def __init__(self,conn,addr):
        self.client = conn
        self.address = addr
        self.name = self.__generate_name()
        self.interact_module = False        # Handle the modue interactive session. This is nit an interactive shell session
        self.default_receive_buffer = 8096  # The dafault buffer size to receive data

    def __generate_name(self,size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    def get_socket(self):
        return self.client
    
    def interactive_module(self):
        self.interact_module = True
        while self.interact_module:
            cmd = input(f"phoenix({self.name})> ")
            self.command_interpreter(cmd)
            
    def send(self,data):
        if not data.endswith('\n'):
            data += '\n'
        self.client.send(data.encode())
            
    def receive(self,length=8096):
        data = self.client.recv(length)
        return data
    
    def receive_all(self):
        recv_len = 1
        response = b''
        s = None
        while recv_len:
            data = self.client.recv(self.default_receive_buffer)
            response += data
            recv_len = len(data)
            if recv_len < self.default_receive_buffer:
                recv_len = 0
                break  
        return response
    def command_interpreter(self,command):
        if len(command) >0:
            if command.startswith(':'):
                if command in [':bg',':exit']:
                    self.interact_module = False
                elif command.startswith('shell'):
                    
                    self.interactive_shell()
                elif command == ':terminate':
                    self.client.close()
                    self.interact_module = False
                elif command == ':help':
                    self.help()
            else:
                self.send(command+"\n")
                data = self.receive_all()
                print(data.decode())
    def check_connection_alive(self):
        if self.client._closed == False:
            return True
        else:
            return False    
    def help(self):
        pass
