import socket, threading

class Netcat2:
    def __init__(self):
        self.RHOST = ''
        self.RPORT = 0
        self.LHOST = ''
        self.LPORT = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.default_recv_len = 1024
        self.server_mode = False
        self.connected_client = None
        self.connected_client_addr = None
        
    def connect(self,rhost,rport):
        self.RHOST = rhost
        self.RPORT = rport
        self.sock.connect((self.RHOST,self.RPORT))
    def listen(self,lhost,lport):
        self.LHOST = lhost
        self.LPORT = lport
        self.server_mode = True
        self.sock.bind((self.LHOST,self.LPORT))
        self.sock.listen(1)
        t = threading.Thread(target=self.__client_accept)
        t.start()
        
    def receive(self,limit=1024):
        if self.server_mode:
            return self.__client_receive(self.connected_client,limit)
        else:
            return self.__client_receive(self.sock,limit)
    def send(self,data):
        if type(data) == type("a"):
            data = data.encode()
        if self.server_mode:
            self.__client_send(self.connected_client,data)
        else:
            self.__client_send(self.sock,data)
    def close(self):
        if self.server_mode:
            self.connected_client.close()
        else:
            self.sock.close()
    def interactive(self,receive_data=True):
        while True:
            cmd = input()
            cmd += "\n"
            self.send(cmd)
            if receive_data:
                rdata = self.receive_all()
                print(rdata.decode(),end=' ')
                
    def receive_all(self):
        recv_len = 1
        response = b''
        s = None
        if self.server_mode:
            s = self.connected_client
        else:
            s = self.sock
            
        while recv_len:
            data = self.__client_receive(s,self.default_recv_len)
            response += data
            recv_len = len(data)
            if recv_len < self.default_recv_len:
                recv_len = 0
                break  
        return response
    def __client_accept(self):
        c, addr = self.sock.accept()
        self.connected_client = c
        self.connected_client_addr = addr
    def __client_receive(self,client,limit=1024):
        return client.recv(limit)

    def __client_send(self,client,data):
        client.send(data)
