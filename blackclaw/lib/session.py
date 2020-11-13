#!/usr/bin/env python3
"""
The Session module for Black Claw
"""
import os, sys
# Get the file current run path
runpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runpath,'..'))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
import string,random
import lib.tcp_server as server
import lib.events as event

class Session:
    def __init__(self):
        self.session_id = 0
        self.session_name = self.__generate_name()
        self.server = None
        self.privilege = ''
        self.session_created = event.EventHook()
        
    
    def set_session_id(self,id):
        self.session_id = id
    def __generate_name(self,size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    def set_server(self,tcp_server):
        self.server = tcp_server
        self.server.session_created +=_server_session_created
    def _server_session_created(self):
        self.session_created.fire()
        
    def run_command(self,command):
        self.server.run_command(command)
    def get_command_result(self,command):
        return self.server.get_command_result(command)
    def interact(self):
        self.server.interact()
    def check_session_alive(self):
        if self.server.client_connection._closed == False:
            return True
        else:
            return False
    def create_server(self,srv_host,srv_port):
        address = srv_host
        port = srv_port
        self.server = server.TCPServer(address,port)
        self.server.session_created +=self._server_session_created
        self.server.run()