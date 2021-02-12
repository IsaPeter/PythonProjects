#!/usr/bin/env python3

import socket, string, random, os, sys, readline
runpath = os.path.dirname(os.path.realpath(__file__))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
sys.path.append(os.path.join(runpath,'..'))
sys.path.append(approot)
import lib.shell as shell
import lib.shm as shm
from lib.helpmenu import HelpMenu
from lib.tabCompleter import tabCompleter

class TCPClient():
    def __init__(self,conn,addr):
        self.client = conn
        self.address = addr
        self.name = self.__generate_name()
        self.interact_module = False        # Handle the modue interactive session. This is nit an interactive shell session
        self.default_receive_buffer = 8096  # The dafault buffer size to receive data
        self.dead = False
        self.maxtimeout = 20                # 20 sec

    def __get_autocomplete_names(self):
        return [':bg',':exit',':terminate',':help']
    def __generate_name(self,size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    def get_socket(self):
        return self.client
    
    def interactive_module(self):
        self.interact_module = True
        t = tabCompleter()
        t.createListCompleter(self.__get_autocomplete_names())        
        readline.set_completer_delims('\t')
        readline.parse_and_bind("tab: complete")   
        readline.set_completer(t.listCompleter) 
        
        try:
            while self.interact_module:
                cmd = input(f"phoenix({self.name})> ")
                cmd = cmd.rstrip(' ')
                if self.dead == False:
                    self.command_interpreter(cmd)
                else:
                    print("[!] The connection is semms to Dead!")
                    self.interactive_module = False
                    break
        except KeyboardInterrupt:
            pass
                
    def send(self,data):
        try:
            if not data.endswith('\n'):
                data += '\n'
            self.client.send(data.encode())
        except BrokenPipeError:
            self.dead = True
        
                
    def receive(self,length=8096):
        try:
            data = self.client.recv(length)
            return data
        except Exception:
            self.dead = True
        
    def receive_all(self):
        try:
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
        except Exception:
            self.dead = True
            
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
            if self.dead == False:
                return True
            else:
                return False
        else:
            self.dead = True
            return False    
    def help(self):
        h = HelpMenu()
        h.inner_heading_row_border = False
        h.title = "Show Client Help"
        h.add_item(':bg, :exit','Exit from the current interactive session')
        h.add_item(':terminate','Terminate the current session')
        h.add_item(':<module_name>','Run a specified module')
        h.add_item(':help','Show this menu')
        h.print_help()